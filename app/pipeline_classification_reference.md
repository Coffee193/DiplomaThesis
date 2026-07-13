# LLM Pipeline Classification Reference

This document describes every classifier in the 5-chain LLM pipeline and whether each output field produces a value from a **predefined set** or is **free-form** (extracted from the user's question).

- **Predefined**: The value MUST come from a fixed, known set of options.
- **Free-form**: The value is extracted/derived from the user's input (e.g., a name, number, or date string).

> Every classifier also outputs a `think` field (free-form, the LLM's reasoning). It is omitted from the tables below for brevity.

---

## Chain 1: Gibberish Detection

### GibberishClassifier

Determines if the user's input is gibberish or a valid question.

| Field | Type | Possible Values |
|-------|------|-----------------|
| `gibberish` | Predefined | `true`, `false` |

---

## Chain 2: High-Level Classification

Chain 2 has multiple sub-classifiers that run conditionally.

### 2a. HighLevelClassifier

Detects whether the question contains the words: job, task, resource.

| Field | Type | Possible Values |
|-------|------|-----------------|
| `words` | Predefined | Subset of `["job", "task", "resource"]` or `[]` |

### 2b. HighLevelOutputJSONClassifier

Only runs if 2a returns `[]`. Detects output-JSON-specific words.

| Field | Type | Possible Values |
|-------|------|-----------------|
| `words` | Predefined | Subset of `["assignment", "dispatch", "duration"]` or `[]` |

### 2c. HighLevelPlanClassifier

Only runs if 2b also returns `[]`. Detects the word "plan".

| Field | Type | Possible Values |
|-------|------|-----------------|
| `words` | Predefined | `["plan"]` or `[]` |

### 2d. HighLevelTaskClassifier

Only runs when 2a returns exactly `["task"]`. Disambiguates which type of task question it is.

| Field | Type | Possible Values |
|-------|------|-----------------|
| `pick` | Predefined | `1` (tasksuitableresources: location/duration), `2` (taskprecedenceconstraints: order/dependencies), `3` (tasks: general) |

### 2e. InputMultiOuputJSONClassifier

Runs when search is `jobs`, `tasks`, or `tasksuitableresources`. Detects time/completion-related words.

| Field | Type | Possible Values |
|-------|------|-----------------|
| `words` | Predefined | Subset of `["complete", "start", "end", "duration", "production", "finish", "done"]` or `[]` |

Note: In the pipeline code, `"production"` is remapped to `"duration"` after extraction.

### 2f. InputMultiOutputJSONDurationLongestShortestClassifier

Only runs when `"duration"` is in `complex`. Detects superlative extremum words.

| Field | Type | Possible Values |
|-------|------|-----------------|
| `pick` | Predefined | `"A"` (longest/most/maximum), `"B"` (shortest/least/minimum), `"None"` (neither) |

### 2g. InputMultiOutputJSONCompleteDateExtractor

Only runs when `"complete"` is in `complex`. Extracts the date from the question.

| Field | Type | Possible Values |
|-------|------|-----------------|
| `date` | Free-form | Extracted date string (e.g., `"November 31"`, `"12/5"`, `"28-2"`, or `""` if none) |

---

## Chain 3: Attribute Retrieval

Determines whether the user is filtering by a specific attribute, and if so, extracts the key and value.

### 3a. JobAttributeRetriever

| Field | Type | Possible Values |
|-------|------|-----------------|
| `attribute` | Predefined | `true`, `false` |
| `key` | Predefined | One of: `"name"`, `"arrivaldate"`, `"duedate"`, `"task"`, `"workcenter"`, `"id"` |
| `value` | Free-form | Extracted from question (e.g., `63`, `"FROM BILLET"`) |

### 3b. ResourceAttributeRetriever

| Field | Type | Possible Values |
|-------|------|-----------------|
| `attribute` | Predefined | `true`, `false` |
| `key` | Predefined | `"name"` or `"id"` |
| `value` | Free-form | Extracted from question (e.g., `7`, `"ROLLING MILL"`) |

### 3c. TaskAttributeRetriever

| Field | Type | Possible Values |
|-------|------|-----------------|
| `attribute` | Predefined | `true`, `false` |
| `key` | Predefined | `"name"` or `"id"` |
| `value` | Free-form | Extracted from question (e.g., `13`, `"MELTING"`) |

### 3d. TasksuitableresourceAttributeRetriever

| Field | Type | Possible Values |
|-------|------|-----------------|
| `attribute` | Predefined | `true`, `false` |
| `know.info` | Predefined | `"resource"` or `"task"` |
| `know.key` | Predefined | `"id"` or `"name"` |
| `know.value` | Free-form | Extracted from question (e.g., `57`, `"MELTSHOP"`) |
| `search.info` | Predefined | `"resource"`, `"task"`, or `"time"` |

### 3e. TaskprecedencecontraintOrderDependenceClassifier

Disambiguates whether the question is about execution order or dependency relationships.

| Field | Type | Possible Values |
|-------|------|-----------------|
| `pick` | Predefined | `"order"` or `"dependence"` |

### 3f. TaskprecedenceconstraintOrderAttributeRetriever

Extracts before/after task IDs for order-type questions.

| Field | Type | Possible Values |
|-------|------|-----------------|
| `attribute` | Predefined | `true`, `false` |
| `before` | Free-form | Task ID (integer) or `"*"` (any/unknown task) |
| `after` | Free-form | Task ID (integer) or `"*"` (any/unknown task) |

### 3g. TaskprecedenceconstraintDependenceAttributeRetriever

Extracts reference/target task IDs for dependency-type questions.

| Field | Type | Possible Values |
|-------|------|-----------------|
| `attribute` | Predefined | `true`, `false` |
| `reference` | Free-form | Task ID (integer) |
| `target` | Free-form | Task ID (integer) or `"*"` (any/unknown task) |

---

## Chain 4: Wanted Return Value

Determines what the user wants returned (which attribute, or the full object).

### 4a. JobAttributeReturnClassifier

| Field | Type | Possible Values |
|-------|------|-----------------|
| `attribute` | Predefined | `true`, `false` |
| `return` | Predefined | One of: `"name"`, `"arrivaldate"`, `"duedate"`, `"task"`, `"workcenter"`, `"id"` |

### 4b. ResourceAttributeReturnClassifier

| Field | Type | Possible Values |
|-------|------|-----------------|
| `attribute` | Predefined | `true`, `false` |
| `return` | Predefined | One of: `"name"`, `"id"`, `"period"` |

### 4c. TaskAttributeReturnClassifier

| Field | Type | Possible Values |
|-------|------|-----------------|
| `attribute` | Predefined | `true`, `false` |
| `return` | Predefined | One of: `"name"`, `"id"` |

### 4d. TasksuitableresourceAttributeReturnResourceClassifier

| Field | Type | Possible Values |
|-------|------|-----------------|
| `attribute` | Predefined | `true`, `false` |
| `key` | Predefined | One of: `"name"`, `"id"`, `"period"` |
| `value` | Free-form | Extracted from question (e.g., `1`, `"ROLLING MILL"`). Optional — only present when the user specifies a specific value. |

### 4e. TasksuitableresourceAttributeReturnTaskClassifier

| Field | Type | Possible Values |
|-------|------|-----------------|
| `attribute` | Predefined | `true`, `false` |
| `key` | Predefined | One of: `"name"`, `"id"`, `"time"` |
| `value` | Free-form | Extracted from question (e.g., `584`, `"ROLLING"`). Optional — only present when the user specifies a specific value. |

---

## Chain 5: Final Answer Generation

### 5a. OutputTaskprecedenceconstraintsClassifyQuestionBoolean

Determines if the question is a yes/no question (for task precedence queries).

| Field | Type | Possible Values |
|-------|------|-----------------|
| `attribute` | Predefined | `true` (yes/no question), `false` (open-ended question) |

### 5b–5k. Answer Formatting Prompts

The remaining Chain 5 modules generate natural-language answers for the user. They do not produce classification values — they take the query results from earlier chains and format them into a response. These are not classifiers and have no predefined output fields.