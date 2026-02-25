# Documents System for Play Palace
Documents are a collection of articles that the user can view to get help or information. Each document has categories and locale support.

Since Play Palace is open source, contributors can edit document .md files directly in the repo. The in-app editor is a nice-to-have for those who do not wish to download the source, or if the file format changes in the future. The in-app editor is not critical to the system.

# Roles
Server admins have full control over document organization and contents. However if only admins had access to the documents system, it would make locale support very difficult.
To account for this, admins can approve people to be transcribers. The transcriber role allows for existing documents to support new translations. Transcribers can not manage documents, or create new ones. They can only create and edit translations.
Transcribers will be assigned a list of languages. They can only modify translations for the languages they are assigned. For example, a transcriber with Spanish and French would not be allowed to create or edit translations of an English version.

## Storing transcriber data
The user table should have a fluent_languages column, which is a list of lang codes (e.g. ["en", "es"]). This tracks what languages a user knows and can be used for purposes beyond translation in the future.

Transcriber assignments should be stored separately, in a transcriber_assignments table (user_id, lang_code). A user may be fluent in a language without being approved as a transcriber for it. This separation also makes queries like "who are the French transcribers?" trivial without parsing JSON arrays.

# Backend folder structure
server/documents/ folder contains each document folder and a "_metadata.json" file.

## Document system metadata file
In the root of the documents folder is a "_metadata.json" file. This file contains:
- Categories dictionary: maps human-readable category slugs to localized display names.

The slug is the internal identifier, set once at creation, and never shown to users. Renaming a category only changes the display name for a specific locale, not the slug. If a locale translation is missing, the system falls back to English, or the slug itself as a last resort.

### Example
```json
{
    "categories": {
        "news": {
            "en": "News and Updates",
            "es": "Noticias y Actualizaciones"
        },
        "game_rules": {
            "en": "Game Rules"
        }
    }
}
```

## Document specific folder
Each document has its own folder, for example "uno_rules".
The folder name IS the document's identity. There is no separate id field in the metadata.
A document's folder contains:
- The content in each locale, e.g. "en.md", "fr.md"
- A "_metadata.json" file

## Document metadata file
Contains the following:
- categories: the list of category slugs this document belongs to.
- source_locale: the original language this document was written in (defaults to "en"). Transcribers use this to detect staleness -- if the source locale's modified_contents is newer than their translation's, they know an update is needed.
- locales: a dictionary of locale codes and settings for each one.

### Locale settings:
- created: the timestamp this locale was created.
- modified_contents: the timestamp for when the document contents of this locale was last modified. This does not include changes to locale settings.
- title: the display title of the document for this locale. Stored in metadata (not in the .md file) so document lists can be displayed without parsing every .md file.
- public: a boolean flag indicating if this locale is visible to normal users. If not, only transcribers and admins can see it.
    - Transcribers of other languages still have viewing access. For example a French transcriber can see the English version even when it is private. This is so the French transcriber knows what changes they need to update before either version is publicly available.
    - A transcriber can only change the visibility for languages they are assigned. For example, a French transcriber can not make an English translation public.

### Example
```json
{
    "categories": ["game_rules"],
    "source_locale": "en",
    "locales": {
        "en": {
            "created": "2026-01-15T10:00:00Z",
            "modified_contents": "2026-02-20T14:30:00Z",
            "title": "Uno Rules",
            "public": true
        },
        "es": {
            "created": "2026-02-01T09:00:00Z",
            "modified_contents": "2026-02-05T11:00:00Z",
            "title": "Reglas de Uno",
            "public": false
        }
    }
}
```

# Loading and data management
Timestamps (created, modified_contents) are stored in metadata JSON, not read from filesystem file attributes. File attributes are unreliable for an open source project -- git does not preserve creation time, and mtime is reset on clone, checkout, and rebase. Contributors editing .md files directly should also update the corresponding _metadata.json. A helper script or pre-commit hook can automate this if it becomes a pain point.

## Startup loading
On server startup, the documents system loads once:
1. Load the root _metadata.json (categories) into memory.
2. Scan each subfolder in server/documents/ and load its _metadata.json into memory.
3. Do NOT load .md content into memory. Document content is loaded on demand when a user views or edits a document.

After startup, all listing, searching, filtering, and title display is served from the in-memory metadata. This keeps memory usage low and startup fast since only small JSON files are read, not every document's full content.

## Writes
When metadata is changed (via the in-app UI or a server command), update both:
- The in-memory state (so changes are reflected immediately)
- The _metadata.json file on disk (so changes persist across restarts)

When document content (.md) is changed via the in-app editor, write directly to disk. There is no in-memory cache for content.

# Still needs design
The following areas need further thought before implementation:

## Deletion and archival
How should documents or individual translations be deleted? Can they be recovered? Should there be a soft-delete / archive mechanism, or is git history sufficient for recovery since the project is open source?

## Document ordering within categories
How are documents ordered when displayed in a category? Options include alphabetical by title, creation date, or a manual sort order field. For game rules, ordering matters -- "How to Play" should appear before "Advanced Strategies."

## Documents with no categories
What happens if a document belongs to zero categories? Should there be an "uncategorized" fallback view, or should the system require at least one category?

## Edit conflicts
What if two people edit the same translation at the same time? Even a simple check -- "the file was modified since you started editing, overwrite?" using the modified_contents timestamp -- would prevent silent data loss.

# Frontend UI structure

## Documents system UI
Add a "Documents" action in the main menu. The documents menu has the following items:
- Category x: display the category name for each category as its own item.
- Manage categories (admins only)
- New document (admins only)
- View transcribers by language
- View transcribers by user

## Documents in category menu
- Filter documents by title: type to narrow the list by document title. Full-text content search can be added later if needed.

## Manage categories menu
Show the list of category names. When clicking on one, ask to rename or delete it.
At the bottom of the menu, add an "add category" item. When creating a category, the admin provides a slug (the permanent internal name) and a display name for their current locale.

## Add document
- Choose categories
- Use the "add translation" flow to create the initial translation. Pass the new document folder name and the current user's locale so it knows what document is being created and can skip choosing a locale.

The folder name is auto-generated from the initial title (slugified). It can be manually renamed on the filesystem if needed, but this is not exposed in the UI.

## View transcribers by language
Shows the standard language menu. Append each item with the number of users assigned to that language.
For example, "English (4 users)"
When clicking on a language, displays the list of users in a menu. If an admin, clicking on a user asks if you want to remove them.
If admin, at the bottom is an "add users" item.
When clicked, shows a list of users who do not have this assigned language, with on/off status.

## View transcribers by user
This is the exact inverse of view transcribers by language.
Shows the list of transcribers as a menu. Append each item with the number of languages assigned to that user.
For example, "Zarvox (4 languages)"
When clicking on a user, displays the list of assigned languages in a menu. If an admin, clicking on a language asks if you want to remove it.
If admin, at the bottom is an "add languages" item.
When clicked, shows the standard language menu excluding the already assigned languages, with on/off status.

## Document actions
When clicking on a document:
- Normal users: automatically view the document (no action menu).
- Transcribers and admins: show a short action menu:
    - View document
    - Edit document
    - Document settings...

"Document settings" opens a submenu with:
- Change title (with language selection)
- Manage visibility (x/x languages public)
- Add translation
- Modify category list (admins only)

Note: The platform does not currently support F2 for inline editing or the context menu key on lists. These would be ideal shortcuts (F2 to jump straight to editing, context key for the settings submenu) and are worth considering as platform features in the future. For now, the three-item action menu keeps things simple and discoverable.

## Language selection menu
After clicking an item that requires language selection, display the list of languages the document has been translated into. Append the created and last modified dates.
Focus the user's current language by default. If their locale is not available for this document, focus on the source locale.
If a transcriber selects edit or change title, only their assigned languages are shown.

## Changing title
Brings up a text field for renaming the document title for the selected locale. This modifies the value in _metadata.json. This does not rename the folder on the backend.

## Manage visibility
Show a list of the document's languages with on/off toggles for public visibility.

## Add translation
Select from the language menu -- only languages the document has NOT been translated into are shown. If a transcriber, further filtered to their assigned languages. If no languages are available, inform them.
Brings up a text field for the title, then a multiline text field for the contents. New translations are private when first created.

## Modifying category list
Shows a menu with each category name and its current status (included / excluded). Pressing enter on an item toggles the status.
