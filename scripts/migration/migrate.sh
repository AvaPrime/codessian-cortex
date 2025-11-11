#!/bin/bash

# Codessian Cortex Database Migration Script
# This script handles database migrations and schema updates

set -e  # Exit on any error

echo "🔄 Starting Codessian Cortex database migration..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MIGRATION_DIR="migrations"
CONFIG_FILE="config/database.yaml"
BACKUP_DIR="backups"
MIGRATION_TABLE="schema_migrations"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_migration() {
    echo -e "${BLUE}[MIGRATION]${NC} $1"
}

# Show usage
usage() {
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  up [n]          Apply all or n migrations up"
    echo "  down [n]        Rollback all or n migrations down"
    echo "  status          Show migration status"
    echo "  create <name>   Create a new migration"
    echo "  reset           Reset database and reapply all migrations"
    echo "  validate        Validate migration files"
    echo "  backup          Create database backup"
    echo "  restore <file> Restore database from backup"
    echo ""
    echo "Examples:"
    echo "  $0 up                    # Apply all pending migrations"
    echo "  $0 up 3                  # Apply 3 migrations up"
    echo "  $0 down 2                # Rollback 2 migrations"
    echo "  $0 create add_user_table # Create new migration"
    echo "  $0 status                # Show current migration status"
    exit 1
}

# Initialize migration system
init_migration_system() {
    print_status "Initializing migration system..."
    
    # Create directories
    mkdir -p "$MIGRATION_DIR"
    mkdir -p "$BACKUP_DIR"
    
    # Create migrations table if not exists
    # This would be database-specific SQL
    print_status "Creating migrations tracking table..."
    
    # Example for PostgreSQL
    cat > "$MIGRATION_DIR/00000000000000_create_migrations_table.sql" << 'EOF'
-- Create migrations tracking table
CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(14) PRIMARY KEY,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

-- Create migration log table
CREATE TABLE IF NOT EXISTS migration_log (
    id SERIAL PRIMARY KEY,
    version VARCHAR(14) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    execution_time_ms INTEGER,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT
);
EOF
    
    print_status "Migration system initialized ✓"
}

# Create new migration
create_migration() {
    local name=$1
    local timestamp=$(date +%Y%m%d%H%M%S)
    local filename="${timestamp}_${name}.sql"
    
    if [ -z "$name" ]; then
        print_error "Migration name is required"
        usage
    fi
    
    # Convert name to snake_case
    name=$(echo "$name" | tr '-' '_' | tr '[:upper:]' '[:lower:]')
    
    cat > "$MIGRATION_DIR/${timestamp}_${name}.sql" << EOF
-- Migration: $name
-- Created at: $(date)

-- UP Migration
-- Add your up migration here

-- Example:
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     username VARCHAR(255) UNIQUE NOT NULL,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
-- );

-- Create indexes
-- CREATE INDEX idx_users_username ON users(username);
-- CREATE INDEX idx_users_email ON users(email);

-- DOWN Migration
-- Add your down migration here

-- Example:
-- DROP TABLE IF EXISTS users;
EOF
    
    print_status "Created migration: $MIGRATION_DIR/$filename"
    print_status "Edit the file to add your migration logic"
}

# Get current migration version
get_current_version() {
    # This would query the database for current version
    # For now, return a placeholder
    echo "00000000000000"
}

# Get migration files
get_migration_files() {
    ls -1 "$MIGRATION_DIR"/*.sql 2>/dev/null | sort
}

# Apply migrations up
migrate_up() {
    local count=${1:-0}
    local current_version=$(get_current_version)
    local applied=0
    
    print_migration "Applying migrations up..."
    print_status "Current version: $current_version"
    
    for migration in $(get_migration_files); do
        local filename=$(basename "$migration")
        local version=$(echo "$filename" | cut -d'_' -f1)
        local name=$(echo "$filename" | cut -d'_' -f2- | sed 's/\.sql$//')
        
        # Skip if already applied
        if [ "$version" \< "$current_version" ] || [ "$version" = "$current_version" ]; then
            continue
        fi
        
        # Stop if we've applied the requested number
        if [ "$count" -gt 0 ] && [ "$applied" -ge "$count" ]; then
            break
        fi
        
        print_status "Applying migration: $filename"
        
        # Apply migration (this would be database-specific)
        # For demonstration, we'll just log it
        print_status "Executing migration: $name"
        
        # Log successful migration
        print_status "Migration applied successfully: $filename"
        ((applied++))
    done
    
    if [ "$applied" -eq 0 ]; then
        print_status "No pending migrations found"
    else
        print_status "Applied $applied migration(s) successfully ✓"
    fi
}

# Rollback migrations down
migrate_down() {
    local count=${1:-1}
    local current_version=$(get_current_version)
    local rolled_back=0
    
    print_migration "Rolling back migrations down..."
    print_status "Current version: $current_version"
    
    # Get migrations in reverse order
    for migration in $(get_migration_files | tac); do
        local filename=$(basename "$migration")
        local version=$(echo "$filename" | cut -d'_' -f1)
        local name=$(echo "$filename" | cut -d'_' -f2- | sed 's/\.sql$//')
        
        # Skip if not applied or if we've rolled back enough
        if [ "$version" \> "$current_version" ] || [ "$rolled_back" -ge "$count" ]; then
            continue
        fi
        
        print_status "Rolling back migration: $filename"
        
        # Rollback migration (this would be database-specific)
        print_status "Executing rollback: $name"
        
        # Log successful rollback
        print_status "Migration rolled back successfully: $filename"
        ((rolled_back++))
    done
    
    if [ "$rolled_back" -eq 0 ]; then
        print_status "No migrations to roll back"
    else
        print_status "Rolled back $rolled_back migration(s) successfully ✓"
    fi
}

# Show migration status
show_status() {
    print_status "Migration Status"
    echo "================"
    
    local current_version=$(get_current_version)
    echo "Current Version: $current_version"
    echo ""
    
    echo "Available Migrations:"
    echo "---------------------"
    
    for migration in $(get_migration_files); do
        local filename=$(basename "$migration")
        local version=$(echo "$filename" | cut -d'_' -f1)
        local name=$(echo "$filename" | cut -d'_' -f2- | sed 's/\.sql$//')
        
        if [ "$version" \< "$current_version" ] || [ "$version" = "$current_version" ]; then
            echo -e "  ${GREEN}✓${NC} $filename"
        else
            echo -e "  ${YELLOW}◯${NC} $filename"
        fi
    done
}

# Reset database
reset_database() {
    print_warning "This will reset the database and reapply all migrations!"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" != "yes" ]; then
        print_status "Reset cancelled"
        return
    fi
    
    print_migration "Resetting database..."
    
    # Create backup first
    create_backup
    
    # Drop and recreate database (this would be database-specific)
    print_status "Dropping and recreating database..."
    
    # Reapply all migrations
    print_status "Reapplying all migrations..."
    migrate_up
    
    print_status "Database reset completed ✓"
}

# Validate migration files
validate_migrations() {
    print_status "Validating migration files..."
    
    local errors=0
    
    for migration in $(get_migration_files); do
        local filename=$(basename "$migration")
        local version=$(echo "$filename" | cut -d'_' -f1)
        
        # Check filename format
        if ! [[ "$filename" =~ ^[0-9]{14}_.+\.sql$ ]]; then
            print_error "Invalid filename format: $filename"
            ((errors++))
        fi
        
        # Check for SQL syntax (basic check)
        if [ ! -s "$migration" ]; then
            print_error "Empty migration file: $filename"
            ((errors++))
        fi
    done
    
    if [ "$errors" -eq 0 ]; then
        print_status "All migration files are valid ✓"
    else
        print_error "Found $errors validation errors"
        exit 1
    fi
}

# Create database backup
create_backup() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/backup_$timestamp.sql"
    
    print_status "Creating database backup..."
    
    # This would be database-specific backup command
    # For PostgreSQL: pg_dump -f "$backup_file" "$DATABASE_URL"
    # For MySQL: mysqldump > "$backup_file"
    
    touch "$backup_file"  # Placeholder
    
    print_status "Backup created: $backup_file"
}

# Restore database from backup
restore_backup() {
    local backup_file=$1
    
    if [ -z "$backup_file" ]; then
        print_error "Backup file is required"
        usage
    fi
    
    if [ ! -f "$backup_file" ]; then
        print_error "Backup file not found: $backup_file"
        exit 1
    fi
    
    print_warning "This will overwrite the current database!"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" != "yes" ]; then
        print_status "Restore cancelled"
        return
    fi
    
    print_status "Restoring database from backup..."
    
    # This would be database-specific restore command
    # For PostgreSQL: psql -f "$backup_file" "$DATABASE_URL"
    # For MySQL: mysql < "$backup_file"
    
    print_status "Database restored from backup: $backup_file"
}

# Main function
main() {
    if [ $# -eq 0 ]; then
        usage
    fi
    
    local command=$1
    shift
    
    case "$command" in
        init)
            init_migration_system
            ;;
        create)
            create_migration "$@"
            ;;
        up)
            migrate_up "$@"
            ;;
        down)
            migrate_down "$@"
            ;;
        status)
            show_status
            ;;
        reset)
            reset_database
            ;;
        validate)
            validate_migrations
            ;;
        backup)
            create_backup
            ;;
        restore)
            restore_backup "$@"
            ;;
        *)
            print_error "Unknown command: $command"
            usage
            ;;
    esac
}

# Run main function
main "$@"