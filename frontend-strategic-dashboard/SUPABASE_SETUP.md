# Supabase Type Generation Setup

## Step 1: Login to Supabase

### Option A: Interactive Login (Recommended)
Open your terminal and run:
```bash
cd /Users/meganharrison/Documents/intelligence_agent/frontend-strategic-dashboard
npx supabase login
```

This will open your browser to authenticate with your Supabase account.

### Option B: Token-based Login
1. Go to https://app.supabase.com/account/tokens
2. Generate a new access token
3. Set it as an environment variable:

```bash
export SUPABASE_ACCESS_TOKEN="your-token-here"
```

Or add to your `.env.local`:
```
SUPABASE_ACCESS_TOKEN=your-token-here
```

## Step 2: Generate Types

Once logged in, run:
```bash
npm run types:generate
```

This will create `src/types/supabase.ts` with all your database types.

## Step 3: Use Generated Types

After generation, you'll have access to:

```typescript
import { Database } from '@/types/supabase'

// Table types
type Project = Database['public']['Tables']['project']['Row']
type ProjectInsert = Database['public']['Tables']['project']['Insert']
type ProjectUpdate = Database['public']['Tables']['project']['Update']

// View types (if any)
type ProjectView = Database['public']['Views']['project_view']['Row']

// Function types (if any)
type FunctionReturn = Database['public']['Functions']['function_name']['Returns']
```

## Step 4: Update Components

Replace manual types with generated ones:

```typescript
// Before
import { Project } from '@/types/project'

// After
import { Database } from '@/types/supabase'
type Project = Database['public']['Tables']['project']['Row']
```

## Benefits
- ✅ Always in sync with database
- ✅ Includes all tables, views, functions
- ✅ Proper null/undefined handling
- ✅ Enums and custom types included
- ✅ Foreign key relationships typed

## Troubleshooting

### If login fails:
```bash
# Check if you're logged in
npx supabase projects list

# If not, try with debug
npx supabase login --debug
```

### If type generation fails:
```bash
# Try with direct database URL
npx supabase gen types typescript --db-url "postgresql://postgres:[YOUR-DB-PASSWORD]@db.vcvwwuctacglcqxqoyne.supabase.co:5432/postgres" > src/types/supabase.ts
```

### Database password location:
Your database password can be found in:
1. Supabase Dashboard → Settings → Database
2. Or in your `.env` file as part of the connection string