# Authoring and project-evolution models

**Status: active candidate design/test semantics; non-normative.**

This document preserves the mathematical responsibilities of the inner and outer
GDOPL models. It is not a second executable authoring procedure, a prerequisite
for using the format, or an independent efficacy certificate.
The [plain-language operator](../../skills/make-genealogy/references/operator.md)
is the sole ordinary executable authoring treatment. The
[specification](../specification.md) and schema retain public conformance authority.
The [experimental package](../../skills/README.md) keeps this mathematical layer
outside ordinary invocation; users do not have to learn its terminology.

## Three responsibilities

| Layer | Responsibility | Authority boundary |
|---|---|---|
| Plain-language operator | Apply the authoring discipline to a bounded repository request | Experimental treatment; does not confer search, write or publication authority |
| Inner GDOPL | Model admissible candidate documents and their target-relative ordering | Active prospective semantics and design/test model, not a competing runtime instruction |
| Outer GDOPL / project-Lagrangian | Evaluate changes to the specification, procedure, documentation, experiments or packaging | Project-level optimisation and disposition, not a genealogy field validator |

## Outer project model

Let $Q_k$ be the accepted project configuration: repository revision,
specification/schema version, authoring procedure, documentation placement,
experiment state and package state. A grounded neighbouring variation is

$$
\eta_k\in\mathcal A_P(Q_k,H_k),
$$

where $H_k$ is the evidence/currentness history and $\mathcal A_P$ contains
only admissible project neighbours. The typed directional response

$$
\Delta_{\eta_k}\mathcal L_P(Q_k)
$$

concerns truthful representation, evidentiary integrity, complexity, authority
surface, maintainer burden, adoption friction, maintenance cost and recoverability.
The notation does not fabricate scalar weights or assume differentiability.
Truth, authority, identity and publication constraints define the feasible set
$\mathcal F_P$. A successor $Q_k\oplus\eta_k$ is admitted only when feasible
and supported by an adequate ordering witness.

A hard-constraint failure blocks admission. A material protected improvement
without material regression supplies a Pareto-style witness. Mixed material
effects require an explicit owner-authorised trade-off, not invented weights.
No demonstrated material improvement can leave the accepted state unchanged or
reject a variation; unresolved distinguishable alternatives can defer admission.
An authorised exploratory construction has its own bounded target and costs;
it is not equivalent to admitting the constructed candidate for use.

Outer dispositions remain:

```text
RETAIN
REJECT
RELOCATE
COMPILE_INTO_STANDARD
UNCHANGED
DEFER_UNRESOLVED
```

Native pre-change intent, a bounded diff, verification evidence and an exact
successor identity can carry an outer actuation. This model does not require a
new runtime ledger or custom intent/receipt schema.

## Inner repository-authoring model

For one repository, let

$$
r_k=(D_k,U_k,E_k,A_k,T).
$$

$D_k$ is the proposed public file, beginning with the existing file when
present. $U_k$ is ephemeral unresolved session state with no publication
authority. $E_k$ is the evidence actually available within scope. $A_k$
bounds inspection, search, drafting, mutation and publication. $T$ is the
bounded authoring target inferred from the request.

The feasible document states

$$
\mathcal D_F(E_k,A_k)
$$

satisfy the pinned standard and hard truth, evidence, precision, authority and
publication constraints. Fabricated facts or precision, resemblance substituted
for reception, dependent surfaces counted independently, unresolved private
material transmitted publicly, and validation claimed as historical or legal
verification are infeasible. Usefulness cannot compensate for such a violation.

For feasible states, the candidate lexicographic partial order is:

1. **Target-bounded semantic adequacy.** Better fulfil $T$, retaining materially
   distinct supported differences in subject, relationship, reception route or
   temporal claim.
2. **Supported specificity.** When target adequacy is equal, use the most
   informative representation actually supported. Relationship values are not
   one universal strength ladder.
3. **Minimality among meaning-equivalent states.** Only when target-relevant
   meaning and supported specificity are equal, reduce redundancy, unnecessary
   breadth, claim surface, maintenance cost and avoidable burden.
4. **Unresolved material non-dominance.** When admissible non-equivalent states
   serve competing material target interests and $T$ does not decide between
   them, ask rather than inventing a scalar comparison.

For a broad create/update request, $T$ covers materially distinct, adequately
supported statements encountered in authorised evidence. It does not imply an
exhaustive genealogy or permit broad external search. A syntax-only or named-
subject target remains correspondingly narrow.

Inner dispositions remain:

```text
KEEP
DROP
NARROW
KEEP_PRIVATE
ASK
STOP
```

Structured public claims, body-only acknowledgements of established but
structurally unrepresentable relationships, and private unresolved candidates
remain different states. Qualification cannot establish source participation.
These boundaries are expressed operationally in the plain-language operator;
the mathematical model neither overrides nor adds a second set of instructions.

## Resolving design value and its limits

The ordinary-language procedure preceded its formal abstraction. The model is
not represented as the historical generator of that initial procedure.
Nevertheless, it exposed the **empty-file attractor**: minimising public output
alone can select truthful omission while failing the requested bounded task.
Adding the target $T$, then applying minimality only among meaning-equivalent
states, resolves that design ambiguity. Repeated source identity is likewise not
semantic redundancy when separate supported claims differ materially.

That is a retained design-level resolving result. It supports the model's active
role in rationale, adversarial test construction and prospective refinement.
It is not a general behavioural-efficacy theorem, proof of an observed execution
pathway, or evidence that a delivery package is operationally superior. Bounded
correct execution, incremental causal advantage and packaging value are separate
questions; neither task-output parity nor lack of observed difference answers
all three.

## Inner/outer coupling

The accepted outer configuration supplies the standard $S_k$ and procedure
$P_k$. Applying them within the authorised repository scope $R$ yields a
trace $T_k$:

$$
G_R(R;S_k,P_k)\rightarrow T_k.
$$

Here $T_k$ denotes a trace, not the bounded target $T$ in the inner state.
The outer process evaluates that trace alongside the accepted configuration:

$$
G_P(Q_k,T_k)\rightarrow Q_{k+1}.
$$

Concretely: an accepted specification/procedure becomes the inner baseline;
repository application may expose friction, a defect or a representational
limit; those traces support a proposed outer variation; an authorised disposition
may then establish the next baseline. A run does not accept its own repair.

The types share concrete-observation/symbolic-alternative feedback, but are not
one state machine and do not share one disposition vocabulary. Canonical
coherence review begins with the existing document, may falsify coherence, and
does not certify efficacy. Review follows material change, not a ceremonial
multi-round loop. A correct-looking answer does not prove this pathway occurred.

## Relationship to the research note

[The Cost of a Decisive Revision: Evidence, Reuse, and Self-Application](../research/README.md)
is a separate anonymous, purpose-agnostic mathematical note. Its finite evidence
model concerns authorised/costed observations and purpose-relative record reuse.
Hosting it here does not make it independent validation of these project models.
Predecessor-governed self-application does not alone imply convergence.

The full historical records, private evaluation worlds, keys, oracle predictions,
raw responses and scorer state remain campaign evidence rather than part of this
public design owner. Their omission from ordinary invocation and this public
projection does not discard the mathematical model or its resolving design value.

```text
USER_MUST_LEARN_GDOPL=NO
OPERATOR_PAGE_USES_GDOPL_VOCABULARY=NO
GDOPL_MATHEMATICS_DISCARDED=NO
INNER_OUTER_GDOPL_COUPLING_PRESERVED=YES
MATHEMATICS_REMAINS_ACTIVE_DESIGN_TEST_MODEL=YES
```
