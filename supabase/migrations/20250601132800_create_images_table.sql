-- Create images table
CREATE TABLE IF NOT EXISTS public.images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID REFERENCES public.posts(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    alt_text TEXT,
    prompt TEXT,
    width INTEGER,
    height INTEGER,
    format TEXT,
    size INTEGER,
    is_featured BOOLEAN DEFAULT FALSE,
    created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_images_post_id ON public.images(post_id);
CREATE INDEX IF NOT EXISTS idx_images_is_featured ON public.images(is_featured);

-- Enable Row Level Security
ALTER TABLE public.images ENABLE ROW LEVEL SECURITY;

-- Create policies for RLS
CREATE POLICY "Enable read access for all users" ON public.images
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for authenticated users only" ON public.images
    FOR INSERT TO authenticated WITH CHECK (true);

CREATE POLICY "Enable update for authenticated users only" ON public.images
    FOR UPDATE TO authenticated USING (auth.uid() = created_by) WITH CHECK (auth.uid() = created_by);

CREATE POLICY "Enable delete for authenticated users only" ON public.images
    FOR DELETE TO authenticated USING (auth.uid() = created_by);

-- Create trigger to update updated_at column
CREATE TRIGGER update_images_updated_at
BEFORE UPDATE ON public.images
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Function to ensure only one featured image per post
CREATE OR REPLACE FUNCTION ensure_single_featured_image()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_featured THEN
        UPDATE public.images 
        SET is_featured = FALSE 
        WHERE post_id = NEW.post_id 
        AND id != NEW.id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to ensure only one featured image per post
CREATE TRIGGER ensure_single_featured_image_trigger
AFTER INSERT OR UPDATE ON public.images
FOR EACH ROW
EXECUTE FUNCTION ensure_single_featured_image();
