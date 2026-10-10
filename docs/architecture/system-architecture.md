# DX system architecture

## 1. Architectural objective

DX Artifacts evolves an imported carrier-focused bootstrap implementation into a deterministic artifact pipeline while preserving the carrier as an independently useful format.

The envelope prototype is the first transport transformation. It must be implemented through reusable artifact, verification, transform, source, and sink boundaries rather than as carrier-specific output formatting inside the CLI handler.

## 2. Layered model

```text
Source adapters
    ↓
Selection engine
    ↓
Artifact constructor
    ↓
Artifact verifier
    ↓
Transform engine
    ↓
Representation verifier
    ↓
Publisher
    ↓
Inspector or application engine
```

A public command may orchestrate several layers. It must not erase their distinct responsibilities.

## 3. Logical components

### 3.1 Source adapters

Source adapters provide workspace candidates or artifact bytes.

Initial source types:

```text
Workspace source
Filesystem file source
Standard-input source
```

A source does not own output naming, overwrite behavior, or publication guarantees.

### 3.2 Selection engine

The selection engine determines which workspace objects may become carrier entries.

It owns:

- candidate discovery;
- explicit operands and scopes;
- include and exclude policy;
- ignore providers;
- binary-content policy;
- source-path safety;
- output self-exclusion when the output is a known filesystem path;
- deterministic candidate ordering;
- selection diagnostics.

It produces a selection report. It does not serialize a carrier.

### 3.3 Carrier constructor

The carrier constructor consumes selected logical paths, exact file bytes, and carrier attributes.

It owns:

- carrier version declaration;
- deterministic entry ordering;
- entry attributes;
- text escaping;
- Base64 representation of binary transported entries;
- trailing-newline representation;
- carrier framing;
- canonical carrier serialization.

It produces exact carrier bytes.

It does not own:

- destination filenames;
- envelope compression;
- envelope-level Base64;
- output overwrite policy;
- filesystem publication.

### 3.4 Artifact verifier

The verifier consumes exact artifact bytes and a verification policy.

It produces:

- success or failure;
- diagnostics classified by layer;
- calculated identities;
- parsed metadata;
- canonicality findings;
- policy findings.

Verification operates over the exact bytes that later stages transform, consume, or publish.

### 3.5 Transform engine

The transform engine converts one artifact representation into another through a registered profile.

The first profile performs:

```text
DX carrier bytes
→ canonical ZIP containing one carrier entry
→ strict Base64
→ DX envelope text
```

Transformation does not change the semantic identity of the inner artifact.

### 3.6 Inspector

The inspector identifies supported representations from physical content and reports their layers.

A future recursive view can expose:

```text
DX envelope
└── ZIP representation
    └── DX carrier
        └── transported entries
```

Inspection never mutates workspace state.

### 3.7 Publisher

The publisher copies a complete, sufficiently verified artifact to an explicit sink.

Initial sinks:

```text
Stdout sink
Filesystem sink
Check or discard sink
```

The sink affects delivery guarantees. It must not affect canonical artifact bytes.

#### Stdout sink

- emits artifact bytes only;
- enables shell composition;
- has no overwrite policy;
- cannot provide atomic filesystem publication.

#### Filesystem sink

- writes through a temporary sibling file;
- flushes and synchronizes as supported;
- atomically replaces as supported;
- rejects unsafe symlink targets;
- enforces output-conflict policy;
- makes exact output self-exclusion possible during selection.

#### Check sink

- consumes complete output internally;
- verifies required properties;
- publishes no artifact;
- supports release gates and preflight validation.

### 3.8 Application engine

The application engine consumes a verified carrier or future workspace-operation artifact.

It owns:

- destination-path policy;
- read-only handling;
- existing-file policy;
- precondition evaluation;
- complete mutation planning;
- safe writes;
- post-operation reporting;
- eventual transactional behavior.

Decoding an envelope is not application. Decoding only recovers the exact enclosed artifact bytes.

## 4. Core domain model

The following pseudocode describes architectural contracts, not a committed Python API:

```python
@dataclass(frozen=True)
class ArtifactDescriptor:
    media_type: str
    format_version: str
    logical_name: str | None
    size: int
    sha256: str


@dataclass(frozen=True)
class Artifact:
    descriptor: ArtifactDescriptor
    stream: BinaryIO


class ArtifactSource(Protocol):
    def open(self) -> BinaryIO:
        ...


class ArtifactSink(Protocol):
    def publish(
        self,
        artifact: Artifact,
        policy: PublicationPolicy,
    ) -> DeliveryReport:
        ...


class ArtifactTransformer(Protocol):
    def transform(
        self,
        source: Artifact,
        profile: TransformProfile,
    ) -> Artifact:
        ...


class ArtifactVerifier(Protocol):
    def verify(
        self,
        source: ArtifactSource,
        policy: VerificationPolicy,
    ) -> VerificationReport:
        ...
```

Concrete implementations may use immutable bytes, spooled streams, or temporary files. The contract concerns exact bytes, not one storage mechanism.

## 5. Dependency direction

Dependencies flow inward toward stable domain contracts:

```text
CLI parsing
    ↓
Use-case orchestration
    ↓
Artifact, verification, transform, source, and sink interfaces
    ↓
Carrier and envelope codecs
    ↓
Filesystem and stream adapters
```

Required constraints:

- Carrier serialization does not depend on CLI argument objects.
- Envelope serialization does not depend on workspace selection.
- Filesystem publication is not embedded in carrier generation.
- Reports are not mixed into artifact byte streams.
- Output paths do not define artifact identity.

## 6. Production flows

### 6.1 Bare carrier

```text
Workspace source
→ selection report
→ carrier serialization spool
→ carrier verification
→ artifact publication
```

### 6.2 Integrated envelope

```text
Workspace source
→ selection report
→ carrier serialization spool
→ carrier verification
→ canonical envelope transformation
→ envelope verification
→ artifact publication
```

### 6.3 Standalone envelope

```text
Carrier source
→ carrier verification
→ canonical envelope transformation
→ envelope verification
→ artifact publication
```

### 6.4 Unwrap

```text
Envelope source
→ envelope parse
→ strict payload decode
→ compressed-representation verification
→ safe ZIP validation
→ exact carrier extraction
→ carrier-identity verification
→ carrier verification
→ artifact publication
```

### 6.5 Inspection

```text
Artifact source
→ physical-content detection
→ layered parsing
→ requested verification policy
→ human or machine-readable report
```

### 6.6 Controlled application

```text
Carrier source
→ carrier verification
→ destination-policy evaluation
→ complete mutation plan
→ precondition verification
→ staged writes
→ commit
→ post-application verification and receipt
```

Transactional commit and delta semantics require later specifications.

## 7. Serialize-once invariant

Integrated envelope production must not:

```text
serialize carrier
→ verify
→ discard
→ reread workspace
→ serialize carrier again
→ envelope
```

It must:

```text
read selected source bytes
→ serialize carrier once
→ verify those exact bytes
→ envelope those exact bytes
→ verify the envelope
→ publish final bytes
```

This prevents duplicate work, time-of-check/time-of-use divergence, and disagreement between verified and enveloped bytes.

## 8. Spooling and bounded resources

Header-first envelope metadata requires carrier and compressed-payload sizes and hashes before final framing is emitted.

The implementation should use binary spooling:

```text
write in memory up to a configured threshold
→ spill to temporary storage beyond the threshold
→ rewind
→ verify exact bytes
→ transform or publish
```

The architecture must not require complete artifacts to remain in memory.

Envelope decoding and decompression must enforce configured limits before unbounded materialization.

## 9. Exact composition invariant

Under identical effective options and stable source state:

```bash
dx pack SOURCE --format envelope
```

must produce the same bytes as:

```bash
dx pack SOURCE |
  dx envelope
```

The integrated implementation may optimize repeated parsing only when equivalent verification is preserved and the resulting bytes remain identical.

## 10. Active output and report separation

Following WP-10 activation, artifact-producing commands follow this contract:

```text
No -o supplied     → artifact to stdout
-o -               → artifact to stdout
-o FILE            → atomic filesystem publication
```

Stdout contains only artifact bytes.

Diagnostics use stderr. Machine-readable operation reports use an explicit report sink. A report is not part of the produced artifact unless a separate format specification explicitly defines it as one.

## 11. Verification layers

The architecture supports successively stronger verification:

```text
Parse
  ↓
Integrity
  ↓
Canonicality
  ↓
Policy
  ↓
Authenticity
  ↓
Application authorization
```

Success at one layer does not imply success at a later layer.

Envelope v1 requires parse and integrity verification. Canonical production additionally requires profile compliance. Authenticity and application authorization remain separate concerns.

## 12. Evolution constraints

Future work must preserve these constraints:

1. Carrier semantics remain distinct from envelope mechanics.
2. Envelope versioning remains independent from carrier versioning.
3. Profiles are versioned contracts, not arbitrary flag combinations.
4. Canonical artifact bytes are independent of the output sink.
5. Integrated commands remain equivalent to explicit stage composition.
6. Inspection does not mutate state.
7. Decoding does not imply application.
8. Integrity does not imply authenticity or authorization.
9. New application operations require explicit semantics and preconditions.
10. Speculative capabilities do not become normative without a specification and accepted decision.

## 13. Repository and runtime boundary

DX Artifacts exposes native product behavior through the `dx_artifacts` package, the `dx` console command, `python -m dx_artifacts`, and a generated standalone `dx.py` release artifact. These forms share one source authority and applicable observable contracts.

The initial repository state imports an external monolith as bootstrap evidence. Later extraction changes native dependency direction without changing accepted behavior unless a separately accepted change authorizes the difference. Dx.Domain and Collab remain external evidence sources and prospective consumers; they do not participate in native generic product ownership.
