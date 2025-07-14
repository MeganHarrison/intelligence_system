#!/bin/bash

# Supabase Type Generation Helper Script

echo "🚀 Supabase Type Generation Setup"
echo "================================="

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo "❌ Supabase CLI not found globally"
    echo "Using local npx version..."
    SUPABASE_CMD="npx supabase"
else
    echo "✅ Supabase CLI found"
    SUPABASE_CMD="supabase"
fi

# Check if logged in
echo ""
echo "🔐 Checking Supabase authentication..."
if $SUPABASE_CMD projects list &> /dev/null; then
    echo "✅ Already logged in to Supabase"
else
    echo "❌ Not logged in to Supabase"
    echo ""
    echo "Please run one of the following:"
    echo "1. $SUPABASE_CMD login"
    echo "2. Export SUPABASE_ACCESS_TOKEN environment variable"
    echo ""
    echo "Get your token from: https://app.supabase.com/account/tokens"
    exit 1
fi

# Generate types
echo ""
echo "📝 Generating TypeScript types..."
$SUPABASE_CMD gen types typescript --project-id vcvwwuctacglcqxqoyne > src/types/supabase.ts

if [ $? -eq 0 ]; then
    echo "✅ Types generated successfully!"
    echo "📄 Output: src/types/supabase.ts"
    
    # Show summary
    echo ""
    echo "📊 Generated types summary:"
    echo "------------------------"
    grep -E "export type|export interface" src/types/supabase.ts | head -10
    echo "... and more"
    
    echo ""
    echo "🎯 Next steps:"
    echo "1. Update your components to use the generated types"
    echo "2. Import types like: import { Database } from '@/types/supabase'"
    echo "3. Use table types: type Project = Database['public']['Tables']['project']['Row']"
else
    echo "❌ Type generation failed"
    echo ""
    echo "Try running with debug:"
    echo "$SUPABASE_CMD gen types typescript --project-id vcvwwuctacglcqxqoyne --debug"
fi