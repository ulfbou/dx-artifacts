# Future consumer transition

## Position in the product lifecycle

Dx.Domain and Collab are prospective external consumers. Their migrations begin only after DX Artifacts has:

- accepted its bootstrap baseline;
- established supported distribution forms;
- produced a versioned consumer-ready release;
- published release identity and digest evidence;
- defined the applicable compatibility contract.

Consumer transition is downstream of DX Artifacts product development. It is not part of native package decomposition and does not block WP-01 through WP-10.

## Dx.Domain adoption

Target relationship:

```text
Dx.Domain release gate
→ pinned DX Artifacts standalone artifact or installed distribution
→ Dx.Domain-specific handoff construction and verification
```

Dx.Domain retains release-gate orchestration, release-evidence selection, feedback dossier semantics, handoff policy, gate-result reporting, and consumer integration tests.

It ceases independent evolution of generic carrier grammar, generic parser and serializer behavior, and generic CLI behavior after adoption.

Migration evidence proves existing release-gate handoffs against the pinned upstream release before the independently maintained generic copy is retired or retained only as attributed historical evidence.

## Collab adoption

Target relationship:

```text
Collab workflow
→ Collab-specific adapter where required
→ pinned DX Artifacts release
```

Collab retains collaboration orchestration, selection and evidence policies, supported historical command adapters, and consumer integration tests.

It ceases independent evolution of the generic codec and new production of historical carrier formats after adoption. Historical behavior remains compatibility evidence and is implemented only where the DX Artifacts compatibility policy explicitly carries it forward.

## Independent transitions

Dx.Domain and Collab migrate independently. A successful transition by one consumer does not claim success for the other.

Each transition records the pinned DX Artifacts version, release identity, digest, installation or acquisition mechanism, applicable consumer tests, coexistence or rollback plan, and disposition of the former generic implementation.
