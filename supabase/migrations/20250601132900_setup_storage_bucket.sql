-- Create storage bucket for blog images
INSERT INTO storage.buckets (id, name, public)
VALUES ('blog-images', 'blog-images', true)
ON CONFLICT (id) DO NOTHING;

-- Create storage policies for the blog-images bucket
CREATE POLICY "Public Access" ON storage.objects FOR SELECT
USING (bucket_id = 'blog-images');

CREATE POLICY "Authenticated users can upload images" ON storage.objects
FOR INSERT TO authenticated
WITH CHECK (bucket_id = 'blog-images');

CREATE POLICY "Users can update their own images" ON storage.objects
FOR UPDATE TO authenticated
USING (auth.uid() = owner)
WITH CHECK (bucket_id = 'blog-images' AND auth.uid() = owner);

CREATE POLICY "Users can delete their own images" ON storage.objects
FOR DELETE TO authenticated
USING (bucket_id = 'blog-images' AND auth.uid() = owner);

-- Create a function to get the storage URL
CREATE OR REPLACE FUNCTION public.get_image_url(storage_path TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN concat('https://', (SELECT storage.buckets.name FROM storage.buckets WHERE id = 'blog-images'), '.supabase.co/storage/v1/object/public/blog-images/', storage_path);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create a function to handle file uploads and update the images table
CREATE OR REPLACE FUNCTION public.handle_new_image()
RETURNS TRIGGER AS $$
DECLARE
    image_url TEXT;
    file_meta JSONB;
    image_id UUID;
BEGIN
    -- Get file metadata
    SELECT meta INTO file_meta
    FROM storage.objects
    WHERE id = NEW.id;
    
    -- Generate the public URL
    image_url := public.get_image_url(NEW.name);
    
    -- Insert into images table if it's a new upload (not an update)
    IF TG_OP = 'INSERT' THEN
        INSERT INTO public.images (
            url,
            alt_text,
            width,
            height,
            format,
            size,
            created_by
        ) VALUES (
            image_url,
            NULL, -- alt_text can be updated later
            (file_meta->>'width')::integer,
            (file_meta->>'height')::integer,
            (file_meta->>'mimetype')::text,
            NEW.metadata->>'size',
            NEW.owner
        )
        RETURNING id INTO image_id;
        
        -- Store the image_id in the storage object's metadata for reference
        UPDATE storage.objects
        SET metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object('image_id', image_id::text)
        WHERE id = NEW.id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new file uploads
DROP TRIGGER IF EXISTS on_image_upload ON storage.objects;
CREATE TRIGGER on_image_upload
AFTER INSERT ON storage.objects
FOR EACH ROW
WHEN (NEW.bucket_id = 'blog-images')
EXECUTE FUNCTION public.handle_new_image();

-- Create a function to delete associated storage objects when an image is deleted from the images table
CREATE OR REPLACE FUNCTION public.delete_storage_object()
RETURNS TRIGGER AS $$
BEGIN
    -- Extract the file path from the URL
    DELETE FROM storage.objects 
    WHERE bucket_id = 'blog-images' 
    AND storage.objects.metadata->>'image_id' = OLD.id::text;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for image deletion
DROP TRIGGER IF EXISTS on_image_delete ON public.images;
CREATE TRIGGER on_image_delete
BEFORE DELETE ON public.images
FOR EACH ROW
EXECUTE FUNCTION public.delete_storage_object();

-- Grant necessary permissions
GRANTE USAGE ON SCHEMA storage TO authenticated, anon;
GRANT ALL ON ALL TABLES IN SCHEMA storage TO authenticated, anon;
GRANT ALL ON ALL SEQUENCES IN SCHEMA storage TO authenticated, anon;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA storage TO authenticated, anon;
