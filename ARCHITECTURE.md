# Application Flow Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FACIAL RECOGNITION APPLICATION                      │
│                                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │   Left Panel     │  │  Center Panel    │  │   Right Panel    │         │
│  │  ────────────    │  │  ─────────────   │  │  ─────────────   │         │
│  │                  │  │                  │  │                  │         │
│  │  ┌────────────┐  │  │  Recognition     │  │  ┌────────────┐  │         │
│  │  │  Camera    │  │  │  Status:         │  │  │ Gestione   │  │         │
│  │  │  Preview   │  │  │  • Detected      │  │  └────────────┘  │         │
│  │  │            │  │  │  • Recognized    │  │                  │         │
│  │  │  [Live     │  │  │  • Unknown       │  │  ┌────────────┐  │         │
│  │  │   Video]   │  │  │                  │  │  │ Settings   │  │         │
│  │  │            │  │  │  User Info:      │  │  └────────────┘  │         │
│  │  │  Face Box  │  │  │  • Name          │  │                  │         │
│  │  │  + Label   │  │  │  • Similarity    │  │  ┌────────────┐  │         │
│  │  └────────────┘  │  │  • Statistics    │  │  │    Exit    │  │         │
│  │                  │  │                  │  │  └────────────┘  │         │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Application Flow

### 1. Startup Sequence

```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Initialize:      │
│ • Database       │
│ • Face Detector  │
│ • Face Embedder  │
│ • Face Matcher   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Load Known Users │
│ • Read database  │
│ • Load embeddings│
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Start Camera    │
│  Start Detection │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Show Main UI    │
└──────────────────┘
```

### 2. Face Detection Loop

```
┌────────────────────────────────────────────────────────────┐
│                    CONTINUOUS LOOP                         │
│                                                            │
│  ┌──────────────┐                                         │
│  │ Capture      │                                         │
│  │ Frame        │                                         │
│  └──────┬───────┘                                         │
│         │                                                  │
│         ▼                                                  │
│  ┌──────────────┐      No                                 │
│  │ Face         ├──────────────┐                         │
│  │ Detected?    │              │                         │
│  └──────┬───────┘              │                         │
│         │ Yes                  │                         │
│         ▼                      ▼                         │
│  ┌──────────────┐      ┌──────────────┐                 │
│  │ Extract      │      │ Display      │                 │
│  │ Face Region  │      │ "No Face"    │                 │
│  └──────┬───────┘      └──────────────┘                 │
│         │                      │                         │
│         ▼                      │                         │
│  ┌──────────────┐              │                         │
│  │ Generate     │              │                         │
│  │ Embedding    │              │                         │
│  └──────┬───────┘              │                         │
│         │                      │                         │
│         ▼                      │                         │
│  ┌──────────────┐              │                         │
│  │ Compare with │              │                         │
│  │ Known Users  │              │                         │
│  └──────┬───────┘              │                         │
│         │                      │                         │
│    ┌────┴────┐                 │                         │
│    │         │                 │                         │
│  Match    No Match             │                         │
│    │         │                 │                         │
│    ▼         ▼                 │                         │
│ ┌─────┐  ┌──────────┐          │                         │
│ │Show │  │ Register │          │                         │
│ │Name │  │ Prompt   │          │                         │
│ └─────┘  └──────────┘          │                         │
│    │         │                 │                         │
│    └─────────┴─────────────────┘                         │
│              │                                            │
│              ▼                                            │
│       ┌──────────────┐                                   │
│       │ Loop Repeat  │                                   │
│       └──────────────┘                                   │
└────────────────────────────────────────────────────────────┘
```

### 3. User Registration Flow

```
┌────────────────┐
│ Unknown Face   │
│   Detected     │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Check Cooldown │
└───────┬────────┘
        │
        ▼
┌────────────────┐         ┌──────────────┐
│ Show           │         │   User       │
│ Registration   │◄────────┤   Clicks     │
│ Dialog         │         │  "Salva"     │
└───────┬────────┘         └──────────────┘
        │
        ▼
┌────────────────┐
│ Validate Input │
│ • Nome filled  │
│ • Cognome OK   │
│ • No duplicate │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Save Photo     │
│ to data/users/ │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Save Embedding │
│ to data/embed/ │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Insert to DB   │
│ (nome, cognome,│
│  paths)        │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Reload Known   │
│ Users List     │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Show Success   │
│   Message      │
└────────────────┘
```

### 4. User Management Flow

```
┌────────────────┐
│ User Clicks    │
│  "Gestione"    │
└───────┬────────┘
        │
        ▼
┌────────────────────────────────┐
│  Management Dialog Opens       │
│                                │
│  ┌──────────────────────────┐  │
│  │  User List with Photos   │  │
│  │  • ID                    │  │
│  │  • Name                  │  │
│  │  • Thumbnail             │  │
│  └──────────────────────────┘  │
│                                │
│  [Add] [Delete] [Close]        │
└────┬───────────────────┬───────┘
     │                   │
  Add User           Delete User
     │                   │
     ▼                   ▼
┌──────────┐      ┌────────────┐
│ Manual   │      │ Select User│
│ Entry    │      │ Confirm    │
│ Dialog   │      │ Delete     │
└────┬─────┘      └─────┬──────┘
     │                  │
     ▼                  ▼
┌──────────┐      ┌────────────┐
│ Register │      │ Remove from│
│ New User │      │ Database   │
└──────────┘      │ Delete     │
                  │ Files      │
                  └────────────┘
```

### 5. Face Recognition Process

```
Input: Face Image
  │
  ▼
┌─────────────────────────────────────┐
│ PREPROCESSING                        │
│ • Resize to 160x160                 │
│ • Normalize pixels                  │
│ • Convert to RGB                    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ FACENET EMBEDDING GENERATION         │
│ • Input: 160x160x3 image            │
│ • CNN Processing                    │
│ • Output: 128-dim vector            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ SIMILARITY COMPARISON                │
│ For each known user:                │
│   • Calculate cosine similarity     │
│   • Track best match                │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        │             │
  Similarity >   Similarity <
   Threshold      Threshold
        │             │
        ▼             ▼
   ┌────────┐   ┌─────────┐
   │ MATCH  │   │ UNKNOWN │
   │ FOUND  │   │  FACE   │
   └────────┘   └─────────┘
        │             │
        ▼             ▼
   ┌────────┐   ┌─────────┐
   │Display │   │ Prompt  │
   │  Name  │   │Register │
   └────────┘   └─────────┘
```

## Data Storage Structure

```
data/
├── users.db (SQLite Database)
│   └── Table: users
│       ├── id (PRIMARY KEY)
│       ├── nome (TEXT)
│       ├── cognome (TEXT)
│       ├── foto_path (TEXT)
│       ├── embedding_path (TEXT)
│       └── created_at (TIMESTAMP)
│
├── users/
│   ├── user_1234567890_John_Doe.jpg
│   ├── user_1234567891_Jane_Smith.jpg
│   └── ...
│
└── embeddings/
    ├── embedding_1234567890_John_Doe.npy
    ├── embedding_1234567891_Jane_Smith.npy
    └── ...
```

## Component Interaction

```
┌──────────────┐
│ Main Window  │
└──────┬───────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│ Camera      │   │  Database   │
│ Widget      │   │             │
└──────┬──────┘   └──────┬──────┘
       │                 │
       │                 │
       ▼                 ▼
┌──────────────────────────────┐
│   Face Recognition Module    │
│   ─────────────────────────  │
│   ┌──────────┐               │
│   │ Detector │               │
│   └─────┬────┘               │
│         ▼                    │
│   ┌──────────┐               │
│   │ Embedder │               │
│   └─────┬────┘               │
│         ▼                    │
│   ┌──────────┐               │
│   │ Matcher  │               │
│   └──────────┘               │
└──────────────────────────────┘
```

## Key Algorithms

### Face Detection (MediaPipe)
1. Input RGB frame
2. Run MediaPipe detection model
3. Extract bounding box coordinates
4. Return list of face locations

### Face Embedding (FaceNet)
1. Preprocess face image (resize, normalize)
2. Pass through CNN layers
3. Extract feature vector (128-dim)
4. L2 normalize vector
5. Return embedding

### Face Matching (Cosine Similarity)
1. For each known embedding:
   - Calculate: similarity = 1 - cosine_distance
2. Find maximum similarity
3. If similarity > threshold:
   - Return matched user
4. Else:
   - Return unknown

## Performance Characteristics

- **Face Detection**: ~30 FPS
- **Embedding Generation**: ~100ms per face
- **Similarity Comparison**: <1ms per user
- **Total Latency**: ~100-150ms per frame
- **Memory Usage**: ~500MB (base) + embeddings

## Error Handling

```
Application Level
    │
    ├─── Camera Errors
    │    └─── Fallback: Show error message, retry
    │
    ├─── Detection Errors
    │    └─── Fallback: Skip frame, continue
    │
    ├─── Database Errors
    │    └─── Fallback: Log error, show user message
    │
    └─── UI Errors
         └─── Fallback: Dialog with error details
```
