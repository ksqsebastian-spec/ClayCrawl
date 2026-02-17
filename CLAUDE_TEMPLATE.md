# CLAUDE.md – Verbindliche Regeln für Claude Code

**Projekt:** [PROJEKTNAME]  
**Version:** 1.0  
**Status:** VERBINDLICH – Keine Ausnahmen

---

## ⚠️ KRITISCHE ANWEISUNG

Diese Regeln sind **ABSOLUT VERBINDLICH**. Bei jeder Code-Änderung MÜSSEN diese Regeln befolgt werden. Es gibt **KEINE AUSNAHMEN**.

**Bei Unsicherheit:** FRAGEN, nicht raten.

---

## 1. SPRACHE & LOKALISIERUNG

### 1.1 UI-Sprache: [DEUTSCH / ENGLISCH]

```
✅ RICHTIG:
- "[Speichern / Save]"
- "[Erfolgreich gespeichert / Successfully saved]"
- "[Bitte ausfüllen / Please fill in]"

❌ FALSCH:
- Gemischte Sprachen in der UI
- Technische Fehlermeldungen
```

### 1.2 Code-Sprache

| Bereich | Sprache |
|---------|---------|
| UI-Texte | [Deutsch / Englisch] |
| Kommentare | [Deutsch / Englisch] |
| Variablen | Englisch |
| Funktionen | Englisch |
| TypeScript-Typen | Englisch |

### 1.3 Kommentar-Beispiel

```typescript
// [Lädt alle Datensätze aus der Datenbank / Loads all records from database]
async function fetchRecords(): Promise<Record[]> {
  // [Filtert nach aktiven Einträgen / Filters by active entries]
  const { data } = await supabase
    .from('records')
    .select('*')
    .eq('status', 'active');
  
  return data ?? [];
}
```

---

## 2. CODE-ARCHITEKTUR

### 2.1 Datei-Organisation

```
REGEL: Eine Komponente = Eine Datei
REGEL: Keine Datei über 300 Zeilen
REGEL: Bei >300 Zeilen → Aufteilen
```

**Dateinamen:** kebab-case

```
✅ RICHTIG:
user-form.tsx
data-table.tsx
status-badge.tsx

❌ FALSCH:
UserForm.tsx      (Kein PascalCase)
userform.tsx      (Nicht zusammen)
user_form.tsx     (Keine Underscores)
```

### 2.2 Ordnerstruktur – VERBINDLICH

```
/app                    → Nur Seiten (page.tsx, layout.tsx)
/components/ui          → Nur UI-Library Komponenten
/components/[feature]   → Feature-spezifische Komponenten
/components/shared      → Geteilte Komponenten
/components/layout      → Layout-Komponenten
/lib                    → Hilfsfunktionen, Validierung, DB
/hooks                  → Custom React Hooks
/types                  → TypeScript Typen
```

**VERBOTEN:**
- Neue Top-Level-Ordner
- `/utils`, `/helpers`, `/services` (→ gehört in `/lib`)
- Dateien außerhalb der Struktur

### 2.3 Import-Reihenfolge

```typescript
// 1. React/Framework
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

// 2. Externe Libraries
import { useQuery } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { format } from 'date-fns';

// 3. UI Komponenten
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

// 4. Feature Komponenten
import { UserCard } from '@/components/users/user-card';

// 5. Hooks
import { useUsers } from '@/hooks/use-users';

// 6. Lib/Utils
import { supabase } from '@/lib/supabase/client';
import { userSchema } from '@/lib/validations/user';

// 7. Types
import type { User } from '@/types';
```

---

## 3. TYPESCRIPT

### 3.1 Keine `any` Types – NIEMALS

```typescript
// ✅ RICHTIG
function processData(data: User[]): ProcessedUser[] { ... }

// ❌ VERBOTEN
function processData(data: any): any { ... }
```

### 3.2 Explizite Return Types – IMMER

```typescript
// ✅ RICHTIG
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.amount, 0);
}

async function fetchUser(id: string): Promise<User | null> {
  ...
}

// ❌ FALSCH
function calculateTotal(items: Item[]) {  // Fehlender Return Type
  return items.reduce((sum, item) => sum + item.amount, 0);
}
```

### 3.3 Typen zentral definieren

```typescript
// ✅ RICHTIG: In /types/index.ts
export interface User {
  id: string;
  name: string;
  email: string;
}

// In Komponente importieren
import type { User } from '@/types';

// ❌ FALSCH: Lokal in Komponente
interface User {  // NEIN!
  id: string;
}
```

### 3.4 Null-Safety

```typescript
// ✅ RICHTIG
const user = data?.user;
if (!user) {
  return <EmptyState message="[Nicht gefunden / Not found]" />;
}

// ❌ FALSCH
const user = data.user;  // Kann crashen!
```

---

## 4. REACT PATTERNS

### 4.1 Nur funktionale Komponenten

```typescript
// ✅ RICHTIG
export function UserCard({ user }: UserCardProps): JSX.Element {
  return <div>...</div>;
}

// ❌ VERBOTEN
export class UserCard extends React.Component { ... }
```

### 4.2 Props Interface – IMMER

```typescript
// ✅ RICHTIG
interface UserCardProps {
  user: User;
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
  isLoading?: boolean;
}

export function UserCard({ 
  user, 
  onEdit, 
  onDelete,
  isLoading = false 
}: UserCardProps): JSX.Element {
  ...
}

// ❌ FALSCH
export function UserCard(props: any) { ... }
export function UserCard({ user, onEdit }) { ... }  // Fehlende Types
```

### 4.3 Event Handler Naming

```typescript
// ✅ RICHTIG
const handleSubmit = () => { ... };
const handleDelete = () => { ... };
const handleInputChange = () => { ... };

// Props
onSubmit?: () => void;
onDelete?: () => void;
onChange?: () => void;
```

### 4.4 Conditional Rendering

```typescript
// ✅ RICHTIG – Klare Struktur
if (isLoading) {
  return <LoadingSpinner />;
}

if (error) {
  return <ErrorMessage message={error.message} />;
}

if (!data || data.length === 0) {
  return <EmptyState message="[Keine Daten / No data]" />;
}

return <DataTable data={data} />;

// ❌ FALSCH – Verschachtelte Ternaries
return isLoading ? <Spinner /> : error ? <Error /> : data ? <Table /> : <Empty />;
```

---

## 5. FORMULARE

### 5.1 React Hook Form + Zod – IMMER

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { userSchema, type UserFormData } from '@/lib/validations/user';

export function UserForm(): JSX.Element {
  const form = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
    defaultValues: {
      name: '',
      email: '',
    },
  });

  const onSubmit = async (data: UserFormData): Promise<void> => {
    // Verarbeitung
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        {/* Felder */}
      </form>
    </Form>
  );
}
```

### 5.2 Validierungs-Schemas in /lib/validations/

```typescript
// /lib/validations/user.ts
import { z } from 'zod';

export const userSchema = z.object({
  name: z
    .string()
    .min(2, '[Name muss mind. 2 Zeichen haben / Name must have at least 2 characters]'),
  
  email: z
    .string()
    .email('[Ungültige E-Mail / Invalid email]'),
  
  // Weitere Felder...
});

export type UserFormData = z.infer<typeof userSchema>;
```

### 5.3 Fehlermeldungen – NUTZERFREUNDLICH

```typescript
// ✅ RICHTIG
'[Bitte gib einen Namen ein / Please enter a name]'
'[E-Mail-Format ungültig / Invalid email format]'
'[Datei zu groß (max. 10 MB) / File too large (max. 10 MB)]'

// ❌ FALSCH
'Required'
'Invalid'
'Error 422'
```

### 5.4 Auto-Save – PFLICHT FÜR ALLE FORMULARE

```typescript
import { useAutoSave } from '@/hooks/use-auto-save';

export function UserForm(): JSX.Element {
  const form = useForm<UserFormData>({ ... });
  
  // Auto-Save MUSS verwendet werden
  useAutoSave({
    key: 'user-form',
    data: form.watch(),
    onRestore: (data) => form.reset(data),
  });
  
  return ( ... );
}
```

---

## 6. DATENBANK & API

### 6.1 Client-Verwendung

```typescript
// Client-Komponenten ('use client')
import { supabase } from '@/lib/supabase/client';

// Server-Komponenten / API Routes
import { createServerClient } from '@/lib/supabase/server';
```

### 6.2 Queries – IMMER mit Error Handling

```typescript
// ✅ RICHTIG
async function fetchUsers(): Promise<User[]> {
  const { data, error } = await supabase
    .from('users')
    .select('*')
    .eq('status', 'active');
  
  if (error) {
    console.error('[Fehler beim Laden / Error loading]:', error);
    throw new Error('[Daten konnten nicht geladen werden / Could not load data]');
  }
  
  return data ?? [];
}

// ❌ FALSCH
async function fetchUsers() {
  const { data } = await supabase.from('users').select('*');
  return data;  // Error wird ignoriert!
}
```

### 6.3 TanStack Query – FÜR DATA FETCHING

```typescript
// /hooks/use-users.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
    staleTime: 5 * 60 * 1000,  // 5 Minuten
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      toast.success('[Erfolgreich erstellt / Successfully created]');
    },
    onError: (error: Error) => {
      toast.error(error.message);
    },
  });
}
```

---

## 7. ERROR HANDLING

### 7.1 Fehler-Hierarchie

```
1. Validierungsfehler → Inline bei Formularfeld
2. API-Fehler → Toast-Benachrichtigung
3. Kritische Fehler → Error-Boundary mit Fallback-UI
```

### 7.2 Error Messages – ZENTRAL

```typescript
// /lib/errors/messages.ts
export const ERROR_MESSAGES = {
  UNKNOWN: '[Unbekannter Fehler / Unknown error]',
  NETWORK: '[Keine Verbindung / No connection]',
  NOT_FOUND: '[Nicht gefunden / Not found]',
  UNAUTHORIZED: '[Sitzung abgelaufen / Session expired]',
  // Feature-spezifisch
  USER_NOT_FOUND: '[Nutzer nicht gefunden / User not found]',
  USER_CREATE_FAILED: '[Nutzer konnte nicht erstellt werden / Could not create user]',
} as const;
```

### 7.3 Toast-Benachrichtigungen

```typescript
import { toast } from 'sonner';

// Erfolg
toast.success('[Erfolgreich gespeichert / Successfully saved]');

// Fehler
toast.error('[Speichern fehlgeschlagen / Save failed]');

// Mit Aktion
toast.error('[Fehler / Error]', {
  action: {
    label: '[Erneut versuchen / Retry]',
    onClick: () => handleRetry(),
  },
});
```

---

## 8. UI KOMPONENTEN

### 8.1 UI-Library verwenden

```
REGEL: Für Standard-UI IMMER [shadcn/ui / MUI / etc.] verwenden
REGEL: Keine eigenen Button, Input, Select bauen
REGEL: UI-Komponenten NUR in /components/ui/
```

### 8.2 Styling – NUR [TAILWIND / CSS MODULES]

```typescript
// ✅ RICHTIG (Tailwind)
<div className="flex items-center gap-4 p-4 bg-white rounded-lg">
  <Button className="w-full">[Speichern / Save]</Button>
</div>

// ❌ VERBOTEN
<div style={{ display: 'flex' }}>  // Keine Inline-Styles
```

### 8.3 Loading States – IMMER

```typescript
// ✅ RICHTIG
<Button disabled={isLoading}>
  {isLoading ? (
    <>
      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
      [Wird gespeichert... / Saving...]
    </>
  ) : (
    '[Speichern / Save]'
  )}
</Button>

// ❌ FALSCH
<Button disabled={isLoading}>[Speichern / Save]</Button>
```

### 8.4 Empty States – NIE LEER LASSEN

```typescript
// ✅ RICHTIG
if (data.length === 0) {
  return (
    <EmptyState
      icon={<FileIcon />}
      title="[Keine Daten / No data]"
      description="[Lege den ersten Eintrag an / Create your first entry]"
      action={
        <Button asChild>
          <Link href="/new">[Neu erstellen / Create new]</Link>
        </Button>
      }
    />
  );
}

// ❌ VERBOTEN
if (data.length === 0) return null;
if (data.length === 0) return <p>No data</p>;
```

---

## 9. SICHERHEIT

### 9.1 Umgebungsvariablen

```typescript
// ✅ RICHTIG
const apiUrl = process.env.NEXT_PUBLIC_API_URL;

// ❌ VERBOTEN – NIEMALS hartcodiert
const apiUrl = 'https://api.example.com';
const apiKey = 'sk-123...';
```

### 9.2 Server-Secrets trennen

```
NEXT_PUBLIC_*   → Kann im Browser sichtbar sein
Ohne Prefix     → NUR auf Server

REGEL: Sensible Keys NIEMALS mit NEXT_PUBLIC_
```

### 9.3 Input Sanitization

```typescript
// ✅ RICHTIG: Zod validiert automatisch
const schema = z.object({
  name: z.string().trim().min(1),
  email: z.string().email().toLowerCase(),
});

// ❌ VERBOTEN
<div dangerouslySetInnerHTML={{ __html: userInput }} />
```

### 9.4 Datei-Upload Validierung

```typescript
// /lib/validations/file-upload.ts
export const fileUploadSchema = z.object({
  file: z
    .instanceof(File)
    .refine(
      (file) => file.size <= [MAX_SIZE],
      '[Datei zu groß / File too large]'
    )
    .refine(
      (file) => [ALLOWED_TYPES].includes(file.type),
      '[Ungültiges Format / Invalid format]'
    ),
});
```

---

## 10. PERFORMANCE

### 10.1 Lazy Loading

```typescript
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(
  () => import('@/components/heavy-component'),
  { 
    loading: () => <LoadingSpinner />,
    ssr: false
  }
);
```

### 10.2 Bilder optimieren

```typescript
// ✅ RICHTIG
import Image from 'next/image';

<Image 
  src={imageUrl}
  alt="[Beschreibung / Description]"
  width={400}
  height={300}
/>

// ❌ FALSCH
<img src={imageUrl} />
```

### 10.3 Query Stale Time

```typescript
// Daten die sich selten ändern
useQuery({
  queryKey: ['settings'],
  staleTime: 30 * 60 * 1000,  // 30 Min
});

// Daten die sich oft ändern
useQuery({
  queryKey: ['notifications'],
  staleTime: 1 * 60 * 1000,   // 1 Min
});
```

---

## 11. TESTING

### 11.1 E2E Tests – [DEUTSCH / ENGLISCH]

```typescript
import { test, expect } from '@playwright/test';

test.describe('[Nutzerverwaltung / User Management]', () => {
  test('[sollte Nutzer erstellen können / should create user]', async ({ page }) => {
    await page.goto('/users/new');
    await page.fill('[name="name"]', 'Test User');
    await page.click('button[type="submit"]');
    await expect(page.locator('text=[Erfolgreich / Success]')).toBeVisible();
  });
});
```

### 11.2 Test-Selektoren

```typescript
// Komponente
<Button data-testid="submit-form">[Speichern / Save]</Button>

// Test
await page.click('[data-testid="submit-form"]');
```

---

## 12. DOKUMENTATION

### 12.1 Komponenten dokumentieren

```typescript
/**
 * [Zeigt eine Nutzerkarte an / Displays a user card]
 * 
 * @example
 * ```tsx
 * <UserCard 
 *   user={user} 
 *   onEdit={(id) => router.push(`/users/${id}/edit`)}
 * />
 * ```
 */
interface UserCardProps {
  /** [Der anzuzeigende Nutzer / The user to display] */
  user: User;
  /** [Callback bei Bearbeiten / Edit callback] */
  onEdit?: (id: string) => void;
}
```

### 12.2 Komplexe Logik kommentieren

```typescript
/**
 * [Berechnet den Status basierend auf dem Datum / Calculates status based on date]
 * 
 * - [überfällig: Datum in Vergangenheit / overdue: date in past]
 * - [dringend: innerhalb 14 Tage / urgent: within 14 days]
 * - [geplant: weiter in Zukunft / scheduled: further in future]
 */
function calculateStatus(date: Date): Status {
  // ...
}
```

---

## 13. GIT & COMMITS

### 13.1 Commit Messages

```
feat: [Feature hinzugefügt / Added feature]
fix: [Fehler behoben / Fixed bug]
refactor: [Code verbessert / Improved code]
docs: [Dokumentation aktualisiert / Updated docs]
style: [Formatierung / Formatting]
test: [Tests hinzugefügt / Added tests]
chore: [Dependencies / Config]
```

### 13.2 Branch-Namen

```
feature/[feature-name]
fix/[bug-name]
refactor/[scope]
```

---

## 14. VERBOTENE PRAKTIKEN

| Verboten | Warum | Stattdessen |
|----------|-------|-------------|
| `any` Type | Keine Type-Safety | Korrekten Typ definieren |
| Inline Styles | Nicht wartbar | Tailwind/CSS |
| Class Components | Veraltet | Funktionale Komponenten |
| `var` | Veraltet | `const` / `let` |
| `==` | Unsicher | `===` |
| `console.log` in Prod | Unprofessionell | Nur `console.error` für Fehler |
| Hardcoded Strings | Nicht wartbar | Konstanten |
| Leere catch-Blöcke | Fehler versteckt | Mindestens loggen |
| Magic Numbers | Unklar | Benannte Konstanten |
| >300 Zeilen/Datei | Unwartbar | Aufteilen |

---

## 15. CHECKLISTE

### Vor jedem Commit

- [ ] Alle UI-Texte in korrekter Sprache
- [ ] Keine `any` Types
- [ ] Alle Funktionen haben Return Types
- [ ] Error Handling vorhanden
- [ ] Loading States implementiert
- [ ] Empty States implementiert
- [ ] Formular hat Auto-Save
- [ ] Validierung mit Zod
- [ ] Keine console.log
- [ ] Komponente <300 Zeilen
- [ ] Imports sortiert
- [ ] TypeScript Errors = 0

### Vor Feature-Abschluss

- [ ] Feature funktioniert wie im PRD
- [ ] Edge Cases behandelt
- [ ] Responsive (mindestens Desktop)
- [ ] Feedback bei Aktionen (Toast)
- [ ] Dokumentation/Kommentare
- [ ] Tests vorhanden (falls E2E-kritisch)

---

**DIESE REGELN SIND NICHT VERHANDELBAR.**

Bei Fragen: **FRAGE NACH** statt zu raten.
