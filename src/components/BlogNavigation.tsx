import React, { useState } from 'react';
import Link from '@docusaurus/Link';
import clsx from 'clsx';

export default function BlogNavigation(): React.ReactElement {
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    'technical-skills': false,
    'cloud-platforms': false,
    'container-orchestration': false,
    'cicd': false,
    'monitoring': false,
    'iac': false,
    'data': false,
    'programming': false,
    'networking': false,
    'version-control': false,
    'config-management': false,
    'service-mesh': false,
    'linux': false,
  });

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  return (
    <nav
      className="menu thin-scrollbar"
      style={{
        position: 'sticky',
        top: 'calc(var(--ifm-navbar-height) + 1rem)',
        height: 'calc(100vh - var(--ifm-navbar-height) - 2rem)',
        overflowY: 'auto',
        padding: '1rem 0'
      }}
    >
      <ul className="menu__list">
        <li>
          <Link className="menu__link" to="/">
            Welcome
          </Link>
        </li>
        <li>
          <Link className="menu__link menu__link--active" to="/blog">
            Blog
          </Link>
        </li>
        <li>
          <Link className="menu__link" to="/podcasts">
            Podcast
          </Link>
        </li>
        <li>
          <Link className="menu__link" to="/courses">
            Courses
          </Link>
        </li>

        {/* Technical Skills List - Collapsible */}
        <li>
          <button
            className={clsx(
              'menu__link',
              'menu__link--sublist',
              expandedSections['technical-skills'] && 'menu__link--sublist-caret'
            )}
            onClick={() => toggleSection('technical-skills')}
            style={{
              cursor: 'pointer',
              background: 'none',
              border: 'none',
              width: '100%',
              textAlign: 'left',
              padding: '0.5rem 1rem'
            }}
          >
            Technical Skills List
          </button>
          {expandedSections['technical-skills'] && (
            <ul className="menu__list">
              <li>
                <Link className="menu__link" to="/technical">
                  Technical Skills Overview
                </Link>
              </li>

              {/* Cloud Platforms & Services */}
              <li>
                <button
                  className={clsx(
                    'menu__link',
                    'menu__link--sublist',
                    expandedSections['cloud-platforms'] && 'menu__link--sublist-caret'
                  )}
                  onClick={() => toggleSection('cloud-platforms')}
                  style={{
                    cursor: 'pointer',
                    background: 'none',
                    border: 'none',
                    width: '100%',
                    textAlign: 'left',
                    padding: '0.5rem 1rem',
                    paddingLeft: '2rem'
                  }}
                >
                  Cloud Platforms & Services
                </button>
                {expandedSections['cloud-platforms'] && (
                  <ul className="menu__list" style={{ paddingLeft: '1rem' }}>
                    <li><Link className="menu__link" to="/technical/aws">AWS</Link></li>
                    <li><Link className="menu__link" to="/technical/gcp">GCP</Link></li>
                    <li><Link className="menu__link" to="/technical/azure">Azure</Link></li>
                    <li><Link className="menu__link" to="/technical/cloudflare">Cloudflare</Link></li>
                    <li><Link className="menu__link" to="/technical/openstack">OpenStack</Link></li>
                    <li><Link className="menu__link" to="/technical/minio">MinIO</Link></li>
                    <li><Link className="menu__link" to="/technical/localstack">LocalStack</Link></li>
                  </ul>
                )}
              </li>

              {/* Container & Orchestration */}
              <li>
                <button
                  className={clsx(
                    'menu__link',
                    'menu__link--sublist',
                    expandedSections['container-orchestration'] && 'menu__link--sublist-caret'
                  )}
                  onClick={() => toggleSection('container-orchestration')}
                  style={{
                    cursor: 'pointer',
                    background: 'none',
                    border: 'none',
                    width: '100%',
                    textAlign: 'left',
                    padding: '0.5rem 1rem',
                    paddingLeft: '2rem'
                  }}
                >
                  Container & Orchestration
                </button>
                {expandedSections['container-orchestration'] && (
                  <ul className="menu__list" style={{ paddingLeft: '1rem' }}>
                    <li><Link className="menu__link" to="/technical/docker">Docker</Link></li>
                    <li><Link className="menu__link" to="/technical/kubernetes">Kubernetes</Link></li>
                    <li><Link className="menu__link" to="/technical/helm">Helm</Link></li>
                    <li><Link className="menu__link" to="/technical/kustomize">Kustomize</Link></li>
                    <li><Link className="menu__link" to="/technical/operators">Operators</Link></li>
                    <li><Link className="menu__link" to="/technical/podman">Podman</Link></li>
                    <li><Link className="menu__link" to="/technical/containerd">containerd</Link></li>
                    <li><Link className="menu__link" to="/technical/cri-o">CRI-O</Link></li>
                  </ul>
                )}
              </li>

              {/* CI/CD & Automation */}
              <li>
                <button
                  className={clsx(
                    'menu__link',
                    'menu__link--sublist',
                    expandedSections['cicd'] && 'menu__link--sublist-caret'
                  )}
                  onClick={() => toggleSection('cicd')}
                  style={{
                    cursor: 'pointer',
                    background: 'none',
                    border: 'none',
                    width: '100%',
                    textAlign: 'left',
                    padding: '0.5rem 1rem',
                    paddingLeft: '2rem'
                  }}
                >
                  CI/CD & Automation
                </button>
                {expandedSections['cicd'] && (
                  <ul className="menu__list" style={{ paddingLeft: '1rem' }}>
                    <li><Link className="menu__link" to="/technical/jenkins">Jenkins</Link></li>
                    <li><Link className="menu__link" to="/technical/github-actions">GitHub Actions</Link></li>
                    <li><Link className="menu__link" to="/technical/gitlab-ci">GitLab CI</Link></li>
                    <li><Link className="menu__link" to="/technical/circleci">CircleCI</Link></li>
                    <li><Link className="menu__link" to="/technical/argocd">ArgoCD</Link></li>
                    <li><Link className="menu__link" to="/technical/flux">Flux</Link></li>
                    <li><Link className="menu__link" to="/technical/tekton">Tekton</Link></li>
                    <li><Link className="menu__link" to="/technical/buildkite">Buildkite</Link></li>
                  </ul>
                )}
              </li>

              {/* Monitoring & Observability */}
              <li>
                <button
                  className={clsx(
                    'menu__link',
                    'menu__link--sublist',
                    expandedSections['monitoring'] && 'menu__link--sublist-caret'
                  )}
                  onClick={() => toggleSection('monitoring')}
                  style={{
                    cursor: 'pointer',
                    background: 'none',
                    border: 'none',
                    width: '100%',
                    textAlign: 'left',
                    padding: '0.5rem 1rem',
                    paddingLeft: '2rem'
                  }}
                >
                  Monitoring & Observability
                </button>
                {expandedSections['monitoring'] && (
                  <ul className="menu__list" style={{ paddingLeft: '1rem' }}>
                    <li><Link className="menu__link" to="/technical/prometheus">Prometheus</Link></li>
                    <li><Link className="menu__link" to="/technical/grafana">Grafana</Link></li>
                    <li><Link className="menu__link" to="/technical/elasticsearch">Elasticsearch</Link></li>
                    <li><Link className="menu__link" to="/technical/datadog">Datadog</Link></li>
                    <li><Link className="menu__link" to="/technical/newrelic">New Relic</Link></li>
                    <li><Link className="menu__link" to="/technical/loki">Loki</Link></li>
                    <li><Link className="menu__link" to="/technical/jaeger">Jaeger</Link></li>
                    <li><Link className="menu__link" to="/technical/opentelemetry">OpenTelemetry</Link></li>
                  </ul>
                )}
              </li>
            </ul>
          )}
        </li>

        {/* Other main navigation items */}
        <li>
          <Link className="menu__link" to="/portfolio">
            Portfolio
          </Link>
        </li>
        <li>
          <Link className="menu__link" to="/troubleshooting">
            Troubleshooting Examples
          </Link>
        </li>
        <li>
          <Link className="menu__link" to="/system-design">
            System Design Examples
          </Link>
        </li>
        <li>
          <Link className="menu__link" to="/interview-prep">
            Interview Preparation
          </Link>
        </li>
      </ul>
    </nav>
  );
}