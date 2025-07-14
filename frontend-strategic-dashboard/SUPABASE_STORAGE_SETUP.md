# Supabase Storage Setup for Strategic Documents

## Current Issue
The document links aren't working because:
1. Files are stored locally in `/documents/` folder
2. No URLs in the `strategic_documents` table
3. No file storage system configured

## Solution: Supabase Storage + URL Management

### **Option 1: Supabase Storage (Recommended)**

#### **Step 1: Create Storage Bucket**
Go to your Supabase Dashboard → Storage → Create Bucket:

```sql
-- Create storage bucket for documents
INSERT INTO storage.buckets (id, name, public)
VALUES ('strategic-documents', 'strategic-documents', true);
```

Or via Dashboard:
- Bucket name: `strategic-documents`
- Public: ✅ Yes (for easy access)

#### **Step 2: Upload Files to Storage**
```javascript
// Example upload script
const { createClient } = require('@supabase/supabase-js')
const fs = require('fs')

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY)

async function uploadDocument(filePath, fileName) {
  const file = fs.readFileSync(filePath)
  
  const { data, error } = await supabase.storage
    .from('strategic-documents')
    .upload(fileName, file)
    
  if (error) throw error
  
  // Get public URL
  const { data: { publicUrl } } = supabase.storage
    .from('strategic-documents')
    .getPublicUrl(fileName)
    
  return publicUrl
}
```

#### **Step 3: Update Database Schema**
Add URL column to `strategic_documents` table:

```sql
-- Add storage_url column
ALTER TABLE strategic_documents 
ADD COLUMN storage_url TEXT;

-- Add storage_path column for internal reference
ALTER TABLE strategic_documents 
ADD COLUMN storage_path TEXT;

-- Update existing records with storage URLs
UPDATE strategic_documents 
SET storage_url = 'https://vcvwwuctacglcqxqoyne.supabase.co/storage/v1/object/public/strategic-documents/' || source_file
WHERE source_file IS NOT NULL;
```

### **Option 2: External Links (Quick Fix)**

If you want to keep files external, just add URLs:

```sql
-- Add external_url column
ALTER TABLE strategic_documents 
ADD COLUMN external_url TEXT;

-- Update with external URLs (OneDrive, Google Drive, etc.)
UPDATE strategic_documents 
SET external_url = 'https://your-onedrive-link.com/...'
WHERE title = 'Document Name';
```

### **Option 3: Local File Server**

Serve files from your backend:

```python
# Add to api_server.py
from fastapi.staticfiles import StaticFiles

# Mount static files
app.mount("/documents", StaticFiles(directory="../documents"), name="documents")
```

Then URLs would be: `http://localhost:8000/documents/filename.md`

## **Recommended Implementation**

### **1. Database Schema Update**
```sql
-- Add storage columns to strategic_documents
ALTER TABLE strategic_documents 
ADD COLUMN storage_url TEXT,
ADD COLUMN storage_path TEXT,
ADD COLUMN file_url TEXT; -- Flexible field for any URL type
```

### **2. Update API Response**
```python
# In api_server.py DocumentResponse
class DocumentResponse(BaseModel):
    # ... existing fields ...
    storage_url: Optional[str] = None
    file_url: Optional[str] = None  # Primary URL to access file
    
# In transformation logic
document = DocumentResponse(
    # ... existing fields ...
    storage_url=row.get('storage_url'),
    file_url=row.get('file_url') or row.get('storage_url') or row.get('file_path'),
)
```

### **3. Update Frontend Links**
```typescript
// In documents page
const getDocumentLink = (document: StrategicDocument) => {
  // Priority order for URLs
  return document.file_url || 
         document.storage_url || 
         document.file_path ||
         null;
};
```

## **Quick Implementation Steps**

### **For Immediate Fix (Option 3):**

1. **Add file serving to backend:**
```bash
# Add to python-backend/api_server.py
app.mount("/documents", StaticFiles(directory="../documents"), name="documents")
```

2. **Update database to include local URLs:**
```sql
UPDATE strategic_documents 
SET file_url = 'http://localhost:8000/documents/' || source_file
WHERE source_file IS NOT NULL;
```

3. **Test the links:**
```bash
curl http://localhost:8000/documents/2025-07-07%20-%20Alleato%20Group%20-%20CSM.md
```

### **For Production (Option 1 - Supabase Storage):**

1. Create storage bucket in Supabase Dashboard
2. Upload your `/documents/` files to the bucket
3. Update database with storage URLs
4. Update API to return storage URLs

## **File URL Patterns**

### **Supabase Storage:**
```
https://vcvwwuctacglcqxqoyne.supabase.co/storage/v1/object/public/strategic-documents/filename.md
```

### **Local Server:**
```
http://localhost:8000/documents/filename.md
```

### **External (OneDrive/Google Drive):**
```
https://onedrive.live.com/view?id=...
https://drive.google.com/file/d/.../view
```

Which option would you prefer to implement first?