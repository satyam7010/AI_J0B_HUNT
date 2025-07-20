# AI Job Hunt Documentation

This directory contains comprehensive documentation for the AI Job Hunt system.

## Documentation Files

- [API Reference](api-reference.md) - Complete reference for the REST API endpoints
- [Architecture](architecture.md) - System architecture and design principles
- [Configuration](configuration.md) - Detailed configuration options and environment variables
- [Database Schema](database-schema.md) - Database structure and relationships
- [Deployment](deployment.md) - Deployment instructions for various environments
- [Advanced Usage](advanced-usage.md) - Advanced features and usage patterns

## Quick Start

For a quick introduction to the system, see the [main README](../../README.md) in the project root.

## Examples

For code examples and usage patterns, see the [examples directory](../examples/).

## API Reference

The API follows RESTful principles with JSON as the primary data format. All endpoints are prefixed with `/api`.

Key endpoints:

- `/api/resumes` - Resume management
- `/api/jobs` - Job analysis
- `/api/applications` - Application processing
- `/api/dashboard` - Dashboard statistics

For detailed information, see the [API Reference](api-reference.md).

## Configuration

The system is configured using environment variables and settings files. Key configuration areas:

- Database settings
- LLM provider settings
- API server settings
- Frontend settings
- Logging settings
- Job scraper settings

For detailed information, see the [Configuration Guide](configuration.md).

## Architecture

The system follows a modular architecture with distinct components:

- **Agents** - AI agents for resume optimization, job analysis, etc.
- **API** - REST API endpoints for system interaction
- **Models** - Data models for system entities
- **Services** - Core services for various functionalities
- **Utilities** - Helper functions and utilities

For detailed information, see the [Architecture Documentation](architecture.md).
