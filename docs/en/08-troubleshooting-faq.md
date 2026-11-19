# Internal LLM gateway: Troubleshooting and FAQ

<!--
Answers: the problems people actually hit, phrased the way they would describe them, and the questions they ask most.
Reader: users, integrators and support staff.
Owns: symptoms, likely causes and fixes; FAQ answers. Refers to: procedures (07), settings and limits (04), status codes (06 §4), contact details (11 §C).
Detail: one row per symptom, with a fix someone can act on and the role that can apply it. The rows below are likely problems for this design, taken from the comparison analysis: confirm or remove them after the pilot. Add an entry every time a support question or incident repeats.
Fill it in using the writing conventions in ../../README.md. Delete this comment when done.
-->

> Not started: written during build phase

## 1. Common problems

| Symptom (as the user says it) | Likely cause | Fix | Who can fix it |
|---|---|---|---|
| "Claude Code says 401 / unauthorized" | Token helper failed or the token expired; device not compliant (Conditional Access) | Run `litellm-token` by hand and read its error; check Intune compliance | User / Endpoint team |
| "It works in the office but not from home" | Remote access is out of scope; home IPs are not allowlisted [CMP A-13] | Use the office network | — |
| "Connection reset / certificate error" | Secure web gateway is inspecting TLS for the gateway host [CMP A-15] | Check the TLS-inspection exemption | Network team |
| "Request is cut off after about a minute" | A timeout in front of LiteLLM is shorter than the request [CMP §2.7] | Check the client and proxy timeouts against 04 §4.3 | Platform / user |
| "Model not found" | Model name not in the catalog, or not allowed for your team | Check `GET /v1/models` | User / Team admin |
| "Why can't I use model X?" | Not processed in Japan, or not approved yet | See §3 | Product owner |
| "429 Too Many Requests" | User, team or backend limit reached | Wait for `Retry-After`; ask for a higher limit | Team admin |
| "Budget exceeded" | Team budget used up for the period | Request an increase (05 §5.4) | Team admin |
| "My request was blocked by a guardrail" | Content matched a rule | Remove the content; ask security if you think it is wrong | User / Security |
| "My spend is charged to the wrong team" | User is in more than one team group | [fill: team selection rule [CMP V-7]] | Platform admin |
| "My IDE plugin key stopped working" | Virtual key expired | Request a new key | Team admin |
| "Handshake failure" (only if mTLS is adopted) | No Intune certificate, or the tool cannot use the OS certificate store [CMP §2.3.4] | [fill: per-tool steps] | Endpoint team |
| "Proxy will not start" (developers, local stack) | DB unreachable, wrong `DATABASE_URL`, or a licence problem | Check task logs; 04 §2 | Platform |

## 2. Diagnostic steps (when the cause is unclear)

1. Check the status page or `/health/readiness`: [fill: status page URL].
2. Note the time, the user, the tool, and the request ID from the error.
3. Check that the user can reach the host at all: run `curl -v https://llm.corp.example/health/liveliness` from the same machine. A TLS error points to inspection; a timeout points to the allowlist.
4. Search the logs for the request ID: [fill: example query].
5. Check recent deploys and config changes: [fill: links].
6. Still stuck: escalate as in 07 §7, with the details from steps 2–5.

## 3. Frequently asked questions

- **Are my prompts stored or read by anyone?** [default: No, by default. Only metadata is stored. The exception is teams that opted in to content logging, approved by legal [CMP A-10, §2.8].]
- **Does my data leave Japan?** [default: Prompts, responses and everything derived from them (logs, spend data, backups) stay in Tokyo and Osaka [CMP §2.5]. Sign-in data is handled by Entra ID, Okta and Intune, which are outside this scope [CMP A-11].]
- **Can I use GPT / Gemini / model X?** [default: Only when it is processed in Japan and approved. See the catalog in 01 §6.5 and the request process in 05 §5.3.]
- **Can I get my own API key?** [default: Only for tools that cannot run the token command.] Keys expire; the maximum lifetime is in 04 §4.4.
- **Who pays?** [default: Your team, from its budget. See 05 §1.]
- **Can I use it from home?** [default: Not in this phase.]

## 4. Getting help

Contact details are in 11 §C.

| Need | Go to |
|---|---|
| Help with the gateway or your tools | [default: help desk] |
| Integrating with the API | [default: platform engineering] |
| Bug or feature request | [fill: issue tracker and template (11 §B)] |
| Security concern | Security / SOC |
