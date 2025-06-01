-- Create post_versions table
CREATE TABLE IF NOT EXISTS public.post_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES public.posts(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    excerpt TEXT,
    updated_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_post_version UNIQUE (post_id, version_number)
);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_post_versions_post_id ON public.post_versions(post_id);
CREATE INDEX IF NOT EXISTS idx_post_versions_version_number ON public.post_versions(version_number);

-- Enable Row Level Security
ALTER TABLE public.post_versions ENABLE ROW LEVEL SECURITY;

-- Create policies for RLS
CREATE POLICY "Enable read access for all users" ON public.post_versions
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for authenticated users only" ON public.post_versions
    FOR INSERT TO authenticated WITH CHECK (true);

-- Function to create a new version when a post is updated
CREATE OR REPLACE FUNCTION create_post_version()
RETURNS TRIGGER AS $$
DECLARE
    next_version INTEGER;
BEGIN
    -- Get the next version number
    SELECT COALESCE(MAX(version_number), 0) + 1 INTO next_version 
    FROM public.post_versions 
    WHERE post_id = NEW.id;
    
    -- Insert the new version
    INSERT INTO public.post_versions (post_id, version_number, title, content, excerpt, updated_by)
    VALUES (NEW.id, next_version, NEW.title, NEW.content, NEW.excerpt, auth.uid());
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger to create a new version when a post is updated
CREATE TRIGGER create_post_version_trigger
AFTER UPDATE ON public.posts
FOR EACH ROW
WHEN (
    OLD.title IS DISTINCT FROM NEW.title OR
    OLD.content IS DISTINCT FROM NEW.content OR
    OLD.excerpt IS DISTINCT FROM NEW.excerpt
)
EXECUTE FUNCTION create_post_version();
