# Generate Types from Supabase

## Current Status
Currently using **manually defined types** that match the actual database schema observed from API responses.

## To Enable Automatic Type Generation

### 1. Install Supabase CLI globally (if not already done)
```bash
npm install -g supabase
```

### 2. Login to Supabase
```bash
supabase login
```

### 3. Generate types automatically
```bash
npm run types:generate
```

Or manually:
```bash
supabase gen types typescript --project-id vcvwwuctacglcqxqoyne > src/types/supabase.ts
```

## Benefits of Auto-Generated Types

✅ **Always in sync** with database schema  
✅ **No manual maintenance** when database changes  
✅ **Type safety** for all database operations  
✅ **IntelliSense support** for database queries  

## Current Type Mapping

### Database → Frontend
- `project_number` → `id`
- `est_revenue` → `budget` 
- `est_completion` → `end_date`
- All other fields mapped directly

### Files Updated
- `src/types/project.ts` - Contains both database and frontend types
- `src/components/projects/project-card.tsx` - Uses frontend types
- `src/app/projects/page.tsx` - Uses frontend types

## Next Steps
1. Run `supabase login` when you have CLI access
2. Run `npm run types:generate` to get auto-generated types
3. Update components to use the generated types from `src/types/supabase.ts`