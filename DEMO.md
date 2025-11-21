# Napkin Demo Guide

This guide demonstrates how to use Napkin's features.

## Creating a Note

1. Visit the homepage at `http://localhost:8080`
2. You'll see the note creation form with:
   - A large text area for your note content
   - An optional password field
   - An optional expiration time selector

### Example: Basic Note

```markdown
# My Shopping List

- Milk
- Eggs
- Bread
- Coffee

**Remember**: Buy organic!
```

### Example: Code Note

```markdown
# Python Quick Reference

## List Comprehension
\`\`\`python
squares = [x**2 for x in range(10)]
\`\`\`

## Dictionary Creation
\`\`\`python
person = {"name": "John", "age": 30}
\`\`\`
```

## Password Protection

To create a password-protected note:

1. Enter your note content
2. Type a password in the "Password Protection" field
3. Click "Create Note"
4. Share the link - recipients will need the password to view it

**Use Case**: Share sensitive information like:
- Temporary passwords
- Personal information
- Confidential notes

## Auto-Expire

Set an expiration time for your note:

1. Select a duration from the "Auto-Expire" dropdown:
   - 1 hour
   - 6 hours
   - 24 hours (1 day)
   - 7 days
   - 30 days

2. The note will be automatically deleted after this time

**Use Case**: Perfect for:
- Temporary meeting notes
- One-time password sharing
- Time-sensitive information

## Viewing Notes

When someone opens your shared link:

1. **No Password**: Note displays immediately
2. **Password Protected**: A password prompt appears first
3. **View Options**:
   - Toggle between "Rendered" (formatted) and "Raw" (plain text) view
   - Copy the note content to clipboard
   - See view count and expiration time

## Markdown Support

Napkin supports full Markdown syntax:

### Headings
```markdown
# H1
## H2
### H3
```

### Text Formatting
```markdown
**bold text**
*italic text*
~~strikethrough~~
```

### Lists
```markdown
- Unordered list item
- Another item

1. Ordered list item
2. Another item
```

### Links and Images
```markdown
[Link text](https://example.com)
![Image alt text](https://example.com/image.jpg)
```

### Code
```markdown
Inline `code`

\`\`\`python
# Code block
def hello():
    print("Hello, World!")
\`\`\`
```

### Quotes
```markdown
> This is a quote
> Multiple lines
```

### Tables
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
| Data 3   | Data 4   |
```

## API Usage

You can also use Napkin programmatically:

### Create a Note
```bash
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -d '{
    "content": "My note content",
    "password": "optional-password",
    "expire_hours": 24
  }'
```

### Get a Note
```bash
curl http://localhost:5000/api/notes/{note-id}?password=optional-password
```

### Check Note Status
```bash
curl http://localhost:5000/api/notes/{note-id}/check
```

## Tips and Best Practices

1. **Security**: 
   - Use strong passwords for sensitive notes
   - Set short expiration times for sensitive data
   - Never share passwords through the same channel as the note link

2. **Organization**:
   - Use markdown headings to structure long notes
   - Use lists for clarity
   - Use code blocks for technical content

3. **Sharing**:
   - Copy the full URL including the note ID
   - Inform recipients if a password is required
   - Let them know the expiration time

4. **Performance**:
   - Notes are stored in PostgreSQL for reliability
   - Expired notes are automatically cleaned up
   - View counts help you track engagement

## Common Use Cases

1. **Quick Meeting Notes**: Share meeting notes instantly without email
2. **Code Snippets**: Share code with syntax highlighting
3. **Temporary Passwords**: Share credentials that auto-expire
4. **Todo Lists**: Collaborative todo lists with no login
5. **Instructions**: Step-by-step guides with markdown formatting
6. **Ideas**: Quick idea capture and sharing

Enjoy using Napkin! 📝
