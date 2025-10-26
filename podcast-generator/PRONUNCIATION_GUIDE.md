# Podcast Pronunciation Guide

This reference lists technology terms that require pronunciation tags in podcast scripts to ensure correct text-to-speech output.

## How to Use This Guide

When writing or editing podcast scripts, always wrap these terms with the specified SSML tags. The TTS generator will convert these to proper SSML format.

**Format**: `<phoneme alphabet="ipa" ph="pronunciation">Term</phoneme>`

## Technology Terms - Pronunciation Reference

### Cloud Providers & Services

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| AWS | "A W S" | `<say-as interpret-as="characters">AWS</say-as>` | Spell out letter by letter |
| Azure | /ˈæʒər/ | `<phoneme alphabet="ipa" ph="ˈæʒɚ">Azure</phoneme>` | "AZH-er" not "ah-ZOOR" |
| GCP | "G C P" | `<say-as interpret-as="characters">GCP</say-as>` | Google Cloud Platform |
| S3 | "S three" | `S3` | Usually correct by default |
| EC2 | "E C two" | `EC2` | Usually correct by default |
| RDS | "R D S" | `<say-as interpret-as="characters">RDS</say-as>` | Relational Database Service |
| ECS | "E C S" | `<say-as interpret-as="characters">ECS</say-as>` | Elastic Container Service |
| EKS | "E K S" | `<say-as interpret-as="characters">EKS</say-as>` | Elastic Kubernetes Service |
| GKE | "G K E" | `<say-as interpret-as="characters">GKE</say-as>` | Google Kubernetes Engine |
| AKS | "A K S" | `<say-as interpret-as="characters">AKS</say-as>` | Azure Kubernetes Service |

### AWS-Specific Services

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| Lambda | /ˈlæmdə/ | `<phoneme alphabet="ipa" ph="ˈlæmdə">Lambda</phoneme>` | "LAM-duh" |
| Fargate | /ˈfɑrɡeɪt/ | `<phoneme alphabet="ipa" ph="ˈfɑrɡeɪt">Fargate</phoneme>` | "FAR-gate" |
| DynamoDB | /daɪˈnæmoʊ diː biː/ | `<phoneme alphabet="ipa" ph="daɪˈnæmoʊ di bi">DynamoDB</phoneme>` | "die-NAM-oh D-B" |
| ElastiCache | /ɪˈlæstɪˌkæʃ/ | `<phoneme alphabet="ipa" ph="ɪˈlæstɪkæʃ">ElastiCache</phoneme>` | "ee-LAST-ee-cash" |
| Aurora | /əˈrɔrə/ | `<phoneme alphabet="ipa" ph="əˈrɔrə">Aurora</phoneme>` | "uh-ROAR-uh" |
| Redshift | /ˈrɛdʃɪft/ | `<phoneme alphabet="ipa" ph="ˈrɛdʃɪft">Redshift</phoneme>` | "RED-shift" |
| SageMaker | /ˈseɪdʒˌmeɪkər/ | `<phoneme alphabet="ipa" ph="ˈseɪdʒmeɪkɚ">SageMaker</phoneme>` | "SAGE-maker" |
| Bedrock | /ˈbɛdrɑk/ | `Bedrock` | Usually correct |
| CloudFormation | /klaʊd fɔrˈmeɪʃən/ | `CloudFormation` | Usually correct |
| CloudFront | /klaʊd frʌnt/ | `CloudFront` | Usually correct |
| IAM | "I A M" | `<say-as interpret-as="characters">IAM</say-as>` | Identity and Access Management |
| VPC | "V P C" | `<say-as interpret-as="characters">VPC</say-as>` | Virtual Private Cloud |
| NAT | "N A T" | `<say-as interpret-as="characters">NAT</say-as>` | Network Address Translation, NOT "nat" |
| ALB | "A L B" | `<say-as interpret-as="characters">ALB</say-as>` | Application Load Balancer |
| NLB | "N L B" | `<say-as interpret-as="characters">NLB</say-as>` | Network Load Balancer |
| CDK | "C D K" | `<say-as interpret-as="characters">CDK</say-as>` | Cloud Development Kit |
| EMR | "E M R" | `<say-as interpret-as="characters">EMR</say-as>` | Elastic MapReduce |
| ECR | "E C R" | `<say-as interpret-as="characters">ECR</say-as>` | Elastic Container Registry |
| EBS | "E B S" | `<say-as interpret-as="characters">EBS</say-as>` | Elastic Block Store |
| EFS | "E F S" | `<say-as interpret-as="characters">EFS</say-as>` | Elastic File System |

### AWS AI/ML Services

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| Trainium | /treɪˈniːəm/ | `<phoneme alphabet="ipa" ph="treɪˈniəm">Trainium</phoneme>` | "tray-NEE-um" (AWS AI chip) |
| Nova | /ˈnoʊvə/ | `<phoneme alphabet="ipa" ph="ˈnoʊvə">Nova</phoneme>` | "NOH-vuh" (Amazon Nova models) |
| HyperPod | /ˈhaɪpərˌpɑd/ | `HyperPod` | Usually correct |
| SnapStart | /snæp stɑrt/ | `SnapStart` | Usually correct |

### AWS Events & Programs

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| re:Invent | "ray invent" | `<phoneme alphabet="ipa" ph="reɪ ɪnˈvɛnt">re:Invent</phoneme>` | "ray in-VENT" (AWS annual conference) |
| re:Post | "ray post" | `<phoneme alphabet="ipa" ph="reɪ poʊst">re:Post</phoneme>` | "ray post" (AWS Q&A forum) |

### Platform as a Service (PaaS)

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| Heroku | /həˈroʊkuː/ | `<phoneme alphabet="ipa" ph="hɛˈroʊku">Heroku</phoneme>` | "heh-ROH-koo" |
| Vercel | /vɝˈsɛl/ | `<phoneme alphabet="ipa" ph="vɝˈsɛl">Vercel</phoneme>` | "vur-SELL" |
| Netlify | /ˈnɛtlɪfaɪ/ | `<phoneme alphabet="ipa" ph="ˈnɛtlɪfaɪ">Netlify</phoneme>` | "NET-li-fy" |
| Railway | /ˈreɪlweɪ/ | `Railway` | Usually correct |
| Render | /ˈrɛndər/ | `Render` | Usually correct |
| Fly.io | "Fly dot I O" | `Fly.io` | Usually correct |
| Flightcontrol | /ˈflaɪtkənˈtroʊl/ | `Flightcontrol` | Usually correct |

### Container & Orchestration

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| Kubernetes | /ˌkuːbərˈnɛtiːz/ | `<phoneme alphabet="ipa" ph="ˌkubɚˈnɛtiz">Kubernetes</phoneme>` | "coo-ber-NET-ees" (Source: Kubernetes.io) |
| K8s | "Kubernetes" | `K8s` | Pronounce as full "Kubernetes", NOT "K eights" |
| kubectl | /ˈkuːbkənˌtroʊl/ | `<phoneme alphabet="ipa" ph="ˈkubkənˌtroʊl">kubectl</phoneme>` | "coob-control" (NOT "coob-cuttle") |
| etcd | /ɛt siː diː/ | `<phoneme alphabet="ipa" ph="ɛt si di">etcd</phoneme>` | "et see dee" (NOT "etsy-D") |
| kubelet | /ˈkuːblɪt/ | `<phoneme alphabet="ipa" ph="ˈkublɪt">kubelet</phoneme>` | "coob-let" |
| Docker | /ˈdɑkər/ | `Docker` | Usually correct |

### Databases

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| PostgreSQL | /ˈpoʊstɡrɛs kjuː ɛl/ | `<phoneme alphabet="ipa" ph="ˈpoʊstɡrɛs kju ɛl">PostgreSQL</phoneme>` | "POST-gres Q-L" |
| Postgres | /ˈpoʊstɡrɛs/ | `<phoneme alphabet="ipa" ph="ˈpoʊstɡrɛs">Postgres</phoneme>` | "POST-gres" |
| MySQL | /maɪˈɛskjuːˈɛl/ | `MySQL` | Chirp3-HD pronounces naturally (may say "my-S-Q-L" or "my-sequel") |
| SQLite | /ˈɛskjuːˈlaɪt/ | `SQLite` | Chirp3-HD pronounces naturally (usually "S-Q-L-ite") |
| Redis | /ˈrɛdɪs/ | `<phoneme alphabet="ipa" ph="ˈrɛdɪs">Redis</phoneme>` | "RED-iss" |
| MongoDB | /ˈmɑŋɡoʊˌdiːˌbiː/ | `MongoDB` | Usually correct |
| Cassandra | /kəˈsændrə/ | `Cassandra` | Usually correct |
| Elasticsearch | /ɪˈlæstɪksɜrtʃ/ | `<phoneme alphabet="ipa" ph="ɪˈlæstɪksɝtʃ">Elasticsearch</phoneme>` | "ee-LAST-ick-serch" |

### Event Streaming & Messaging

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| Apache Kafka | /əˈpætʃi ˈkɑfkə/ | `<phoneme alphabet="ipa" ph="əˈpætʃi ˈkɑfkə">Apache Kafka</phoneme>` | "uh-PATCH-ee KAF-kuh" |
| Kafka | /ˈkɑfkə/ | `<phoneme alphabet="ipa" ph="ˈkɑfkə">Kafka</phoneme>` | "KAF-kuh" |
| Kinesis | /kɪˈniːsɪs/ | `<phoneme alphabet="ipa" ph="kɪˈnisɪs">Kinesis</phoneme>` | "kih-NEE-sis" |

### Infrastructure as Code

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| Terraform | /ˈtɛrəfɔrm/ | `Terraform` | Usually correct |
| tfsec | "T F sec" | `<say-as interpret-as="characters">TF</say-as>sec` | "T-F sec" NOT "tif-sec" |
| Pulumi | /puːˈluːmi/ | `<phoneme alphabet="ipa" ph="puˈlumi">Pulumi</phoneme>` | "poo-LOO-mee" |
| Ansible | /ˈænsɪbəl/ | `<phoneme alphabet="ipa" ph="ˈænsəbəl">Ansible</phoneme>` | "AN-sih-bull" |
| Chef | /ʃɛf/ | `Chef` | Usually correct |
| Puppet | /ˈpʌpɪt/ | `Puppet` | Usually correct |

### Observability & Monitoring

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| ELK | /ɛlk/ | `<phoneme alphabet="ipa" ph="ɛlk">ELK</phoneme>` | "elk" (like the animal), NOT "E-L-K" |
| Prometheus | /prəˈmiːθiəs/ | `<phoneme alphabet="ipa" ph="prəˈmiθiəs">Prometheus</phoneme>` | "proh-MEE-thee-us" |
| Grafana | /ɡrəˈfɑːnə/ | `<phoneme alphabet="ipa" ph="ɡrəˈfɑnə">Grafana</phoneme>` | "gruh-FAH-nuh" |
| Datadog | /ˈdeɪtədɔɡ/ | `Datadog` | Usually correct |
| OpenTelemetry | /ˈoʊpən tɛˈlɛmɪtri/ | `<phoneme alphabet="ipa" ph="ˈoʊpən tɛˈlɛmɪtri">OpenTelemetry</phoneme>` | "OH-pen teh-LEM-ih-tree" |
| Splunk | /splʌŋk/ | `Splunk` | Usually correct |

### Networking & CDN

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| Cloudflare | /ˈklaʊdflɛər/ | `Cloudflare` | Usually correct |
| Fastly | /ˈfæstli/ | `Fastly` | Usually correct |
| Akamai | /ˈɑːkəmaɪ/ | `<phoneme alphabet="ipa" ph="ˈɑkəmaɪ">Akamai</phoneme>` | "AH-kuh-my" |
| Nginx | /ˈɛndʒɪnˈɛks/ | `<phoneme alphabet="ipa" ph="ˈɛndʒɪn ˈɛks">Nginx</phoneme>` | "engine-X" |
| Apache | /əˈpætʃi/ | `<phoneme alphabet="ipa" ph="əˈpætʃi">Apache</phoneme>` | "uh-PATCH-ee" |
| CDN | "C D N" | `<say-as interpret-as="characters">CDN</say-as>` | Content Delivery Network |
| DNS | "D N S" | `<say-as interpret-as="characters">DNS</say-as>` | Domain Name System |

### Protocols & Standards

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| HTTP | "H T T P" | `<say-as interpret-as="characters">HTTP</say-as>` | Hypertext Transfer Protocol |
| HTTPS | "H T T P S" | `<say-as interpret-as="characters">HTTPS</say-as>` | NOT "H-T-T-P-S" |
| SSH | "S S H" | `<say-as interpret-as="characters">SSH</say-as>` | Secure Shell |
| TCP/IP | "T C P I P" | `<say-as interpret-as="characters">TCP</say-as>/IP` | Transmission Control Protocol |
| API | "A P I" | `<say-as interpret-as="characters">API</say-as>` | Application Programming Interface |
| REST API | "rest A P I" | `REST <say-as interpret-as="characters">API</say-as>` | REpresentational State Transfer |
| OAuth | /ˈoʊɑːθ/ | `<phoneme alphabet="ipa" ph="ˈoʊɑθ">OAuth</phoneme>` | "OH-auth" |
| JWT | "J W T" | `<say-as interpret-as="characters">JWT</say-as>` | JSON Web Token |

### Compliance & Security

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| SOC 2 | "sock two" | `<phoneme alphabet="ipa" ph="sɑk tu">SOC 2</phoneme>` | "sock two" NOT "S-O-C two" |
| HIPAA | "hippa" | `<phoneme alphabet="ipa" ph="ˈhɪpə">HIPAA</phoneme>` | "HIP-uh" NOT "H-I-P-A-A" |
| GDPR | "G D P R" | `<say-as interpret-as="characters">GDPR</say-as>` | General Data Protection Regulation |
| RBAC | "arr back" | `<phoneme alphabet="ipa" ph="ɑr bæk">RBAC</phoneme>` | "arr-back" NOT "R-B-A-C" |

### Acronyms & Abbreviations

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| DevOps | /dɛvɑps/ | `DevOps` | Usually correct ("dev-ops") |
| MLOps | "em-el-ahps" | `<phoneme alphabet="ipa" ph="ɛm ɛl ɑps">MLOps</phoneme>` | "em-el-ahps" NOT "em-lops" or "M-L-ops" |
| AIOps | /ˈeɪaɪɑps/ | `<phoneme alphabet="ipa" ph="ˌeɪ aɪ ɑps">AIOps</phoneme>` | "A-I-ops" |
| FinOps | /fɪnɑps/ | `<phoneme alphabet="ipa" ph="fɪn ɑps">FinOps</phoneme>` | "fin-ops" (Financial Operations) |
| CI/CD | "C I C D" | `<say-as interpret-as="characters">CI</say-as>/<say-as interpret-as="characters">CD</say-as>` | Continuous Integration/Deployment |
| PaaS | /pæs/ | `<phoneme alphabet="ipa" ph="pæs">PaaS</phoneme>` | "pass" (Platform as a Service) |
| IaaS | /ˈaɪæs/ | `<phoneme alphabet="ipa" ph="ˈaɪæs">IaaS</phoneme>` | "EYE-as" (Infrastructure as a Service) |
| SaaS | /sæs/ | `<phoneme alphabet="ipa" ph="sæs">SaaS</phoneme>` | "sass" (Software as a Service) |
| ROI | "R O I" | `<say-as interpret-as="characters">ROI</say-as>` | Return on Investment |
| CLI | "C L I" | `<say-as interpret-as="characters">CLI</say-as>` | Command Line Interface |
| GUI | /ˈɡuːi/ | `<phoneme alphabet="ipa" ph="ˈɡui">GUI</phoneme>` | "GOO-ee" (Graphical User Interface) |
| SQL | /ˈɛskjuːˈɛl/ | `<phoneme alphabet="ipa" ph="ˌɛskjuː ˈɛl">SQL</phoneme>` | "S-Q-L" or "sequel" |
| NoSQL | /noʊˈɛskjuːˈɛl/ | `<phoneme alphabet="ipa" ph="noʊ ˌɛskjuː ˈɛl">NoSQL</phoneme>` | "no S-Q-L" |

### Hardware & Storage

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| GPU | "G P U" | `<say-as interpret-as="characters">GPU</say-as>` | Graphics Processing Unit |
| CPU | "C P U" | `<say-as interpret-as="characters">CPU</say-as>` | Central Processing Unit |
| RAM | /ræm/ | `<say-as interpret-as="characters">RAM</say-as>` | Random Access Memory |
| SSD | "S S D" | `<say-as interpret-as="characters">SSD</say-as>` | Solid State Drive |
| NVMe | "N V M E" | `<say-as interpret-as="characters">NVMe</say-as>` | Non-Volatile Memory Express |
| HDD | "H D D" | `<say-as interpret-as="characters">HDD</say-as>` | Hard Disk Drive |

### Languages & Formats

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| YAML | /ˈjæməl/ | `<phoneme alphabet="ipa" ph="ˈjæməl">YAML</phoneme>` | "YAM-ul" NOT "Y-A-M-L" |
| JSON | /ˈdʒeɪsən/ | `<phoneme alphabet="ipa" ph="ˈdʒeɪsən">JSON</phoneme>` | "JAY-son" |
| XML | "X M L" | `<say-as interpret-as="characters">XML</say-as>` | eXtensible Markup Language |
| HTML | "H T M L" | `<say-as interpret-as="characters">HTML</say-as>` | HyperText Markup Language |
| CSS | "C S S" | `<say-as interpret-as="characters">CSS</say-as>` | Cascading Style Sheets |

### Operating Systems

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| Linux | /ˈlɪnəks/ | `<phoneme alphabet="ipa" ph="ˈlɪnəks">Linux</phoneme>` | "LIN-uks" NOT "LIE-nux" |
| Unix | /ˈjuːnɪks/ | `<phoneme alphabet="ipa" ph="ˈjunɪks">Unix</phoneme>` | "YOU-nix" |

## Usage Examples

### Before (No Pronunciation Tags)
```
Speaker 1: We're deploying Kubernetes on AWS with PostgreSQL as our database.
```

### After (With Pronunciation Tags)
```
Speaker 1: We're deploying <phoneme alphabet="ipa" ph="ˌkubɚˈnɛtɪs">Kubernetes</phoneme> on <say-as interpret-as="characters">AWS</say-as> with <phoneme alphabet="ipa" ph="ˈpoʊstɡrɛs">PostgreSQL</phoneme> as our database.
```

## Automation

Use the pronunciation validation script to check scripts:

```bash
cd podcast-generator
python3 scripts/validate_pronunciations.py ../docs/podcasts/scripts/episode-name.txt
```

This will flag any terms from this guide that appear without pronunciation tags.

## Contributing

If you discover a term that TTS consistently mispronounces:

1. Add it to this guide with IPA pronunciation
2. Update the validation script
3. Add the correction to existing scripts
4. Document in CLAUDE.md

## Resources

- **IPA Phonetic Alphabet**: https://en.wikipedia.org/wiki/International_Phonetic_Alphabet
- **Google Cloud TTS SSML**: https://cloud.google.com/text-to-speech/docs/ssml
- **IPA Converter**: https://tophonetics.com/

## Quick Reference Card

**Most Critical (Always Use These)**:
- Kubernetes → `<phoneme alphabet="ipa" ph="ˌkubɚˈnɛtɪs">Kubernetes</phoneme>`
- PostgreSQL/Postgres → `<phoneme alphabet="ipa" ph="ˈpoʊstɡrɛs">Postgres</phoneme>`
- Azure → `<phoneme alphabet="ipa" ph="ˈæʒɚ">Azure</phoneme>`
- Lambda → `<phoneme alphabet="ipa" ph="ˈlæmdə">Lambda</phoneme>` ("LAM-duh")
- Fargate → `<phoneme alphabet="ipa" ph="ˈfɑrɡeɪt">Fargate</phoneme>` ("FAR-gate")
- DynamoDB → `<phoneme alphabet="ipa" ph="daɪˈnæmoʊ di bi">DynamoDB</phoneme>` ("die-NAM-oh D-B")
- Trainium → `<phoneme alphabet="ipa" ph="treɪˈniəm">Trainium</phoneme>` ("tray-NEE-um")
- re:Invent → `<phoneme alphabet="ipa" ph="reɪ ɪnˈvɛnt">re:Invent</phoneme>` ("ray in-VENT")
- Elasticsearch → `<phoneme alphabet="ipa" ph="ɪˈlæstɪksɝtʃ">Elasticsearch</phoneme>` ("ee-LAST-ick-serch")
- Kafka → `<phoneme alphabet="ipa" ph="ˈkɑfkə">Kafka</phoneme>` ("KAF-kuh")
- MLOps → `<phoneme alphabet="ipa" ph="ɛm ɛl ɑps">MLOps</phoneme>` ("em-el-ahps")
- YAML → `<phoneme alphabet="ipa" ph="ˈjæməl">YAML</phoneme>`
- Nginx → `<phoneme alphabet="ipa" ph="ˈɛndʒɪn ˈɛks">Nginx</phoneme>`
- SOC 2 → `<phoneme alphabet="ipa" ph="sɑk tu">SOC 2</phoneme>` ("sock two")
- HIPAA → `<phoneme alphabet="ipa" ph="ˈhɪpə">HIPAA</phoneme>` ("hippa")
- RBAC → `<phoneme alphabet="ipa" ph="ɑr bæk">RBAC</phoneme>` ("arr-back")
- AWS, GCP, IAM, VPC, NAT, ALB, NLB, ECS, EKS, RDS, API, GPU, CPU → Use `<say-as interpret-as="characters">TERM</say-as>`

---

**Last Updated**: 2025-10-24
**Version**: 1.1.0
