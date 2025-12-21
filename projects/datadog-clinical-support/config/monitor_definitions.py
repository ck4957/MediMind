"""
Monitor definitions for Datadog
"""

MONITOR_DEFINITIONS = [
    {
        'name': 'High Latency on Cancer Risk Assessment',
        'type': 'metric alert',
        'query': 'avg(last_5m):avg:cancer_risk.api.latency{service:cancer-risk-assessment} > 2000',
        'message': '''
Cancer risk assessment API is experiencing high latency (>2 seconds).

This may impact patient care and clinical decision-making.

**Impact:** Delayed risk assessments
**Recommended Actions:**
1. Check Vertex AI endpoint health
2. Review Gemini API response times
3. Investigate database query performance
4. Check for resource constraints

@pagerduty
@slack-clinical-alerts
        '''.strip(),
        'tags': ['service:cancer-risk-assessment', 'priority:high', 'team:clinical-ai'],
        'priority': 1,
        'options': {
            'thresholds': {
                'critical': 2000,
                'warning': 1500,
            },
            'notify_no_data': True,
            'no_data_timeframe': 10,
            'require_full_window': False,
            'notify_audit': False,
            'include_tags': True,
        }
    },
    {
        'name': 'Low Confidence High Risk Prediction',
        'type': 'metric alert',
        'query': 'avg(last_15m):avg:cancer_risk.prediction.confidence{risk_level:high} < 0.7',
        'message': '''
Model is producing high-risk predictions with low confidence (<70%).

**Impact:** Potential for inaccurate risk assessments
**Recommended Actions:**
1. Flag cases for manual clinical review
2. Check model input data quality
3. Verify model version and deployment
4. Consider retraining if pattern persists

@slack-ml-team
        '''.strip(),
        'tags': ['service:cancer-risk-assessment', 'priority:medium', 'team:ml-ops'],
        'priority': 2,
        'options': {
            'thresholds': {
                'critical': 0.7,
                'warning': 0.75,
            },
            'notify_no_data': False,
            'require_full_window': True,
        }
    },
    {
        'name': 'Suspicious Query Pattern Detected',
        'type': 'metric alert',
        'query': 'pct_change(avg(last_5m),last_15m):avg:cancer_risk.queries.rate{service:cancer-risk-assessment} > 200',
        'message': '''
Unusual spike in query rate detected (>200% increase).

**Possible Causes:**
- Legitimate traffic surge
- Potential security incident
- Bot activity
- System misconfiguration

**Immediate Actions:**
1. Review recent query logs
2. Check for suspicious patterns
3. Verify API authentication
4. Monitor for data exfiltration attempts

@security-team
@pagerduty
        '''.strip(),
        'tags': ['service:cancer-risk-assessment', 'priority:high', 'team:security'],
        'priority': 1,
        'options': {
            'thresholds': {
                'critical': 200,
                'warning': 150,
            },
            'notify_no_data': False,
        }
    },
    {
        'name': 'API Rate Limit Warning',
        'type': 'metric alert',
        'query': 'sum(last_5m):sum:cancer_risk.api.rate_limit_errors{*} > 10',
        'message': '''
API rate limiting errors detected.

**Service:** {{service.name}}
**Endpoint:** {{endpoint.name}}

**Impact:** Some requests are being rejected
**Recommended Actions:**
1. Review API usage patterns
2. Consider increasing rate limits
3. Implement request queuing
4. Enable auto-scaling

@devops-team
        '''.strip(),
        'tags': ['service:cancer-risk-assessment', 'priority:medium', 'team:devops'],
        'priority': 3,
        'options': {
            'thresholds': {
                'critical': 10,
                'warning': 5,
            },
        }
    },
    {
        'name': 'Model Accuracy Degradation',
        'type': 'metric alert',
        'query': 'avg(last_1h):avg:cancer_risk.model.accuracy{*} < 0.8',
        'message': '''
Model prediction accuracy has dropped below 80%.

**Critical Alert:** Model performance degradation detected

**Immediate Actions:**
1. Halt automated high-risk predictions
2. Escalate all cases for manual review
3. Investigate data drift
4. Check model versioning
5. Prepare for model rollback if needed

**Do not ignore this alert - patient safety may be at risk.**

@ml-team
@clinical-leadership
@pagerduty
        '''.strip(),
        'tags': ['service:cancer-risk-assessment', 'priority:critical', 'team:ml-ops'],
        'priority': 1,
        'options': {
            'thresholds': {
                'critical': 0.8,
                'warning': 0.85,
            },
            'notify_no_data': True,
            'no_data_timeframe': 60,
            'require_full_window': True,
        }
    },
    {
        'name': 'Gemini API Error Rate High',
        'type': 'metric alert',
        'query': 'sum(last_10m):sum:cancer_risk.gemini.errors{*}.as_rate() > 0.05',
        'message': '''
High error rate detected for Gemini API calls (>5%).

**Impact:** Clinical note analysis may be failing
**Recommended Actions:**
1. Check Gemini API status
2. Verify API credentials
3. Review error messages in logs
4. Implement fallback mechanisms

@devops-team
        '''.strip(),
        'tags': ['service:cancer-risk-assessment', 'priority:high', 'team:devops'],
        'priority': 2,
        'options': {
            'thresholds': {
                'critical': 0.05,
                'warning': 0.03,
            },
        }
    },
    {
        'name': 'Vertex AI Inference Timeout',
        'type': 'metric alert',
        'query': 'sum(last_10m):sum:cancer_risk.vertex_ai.timeouts{*} > 5',
        'message': '''
Multiple Vertex AI inference timeouts detected.

**Impact:** Risk predictions not completing
**Recommended Actions:**
1. Check Vertex AI endpoint health
2. Review model complexity
3. Consider scaling endpoint resources
4. Implement timeout retry logic

@ml-ops
        '''.strip(),
        'tags': ['service:cancer-risk-assessment', 'priority:high', 'team:ml-ops'],
        'priority': 2,
        'options': {
            'thresholds': {
                'critical': 5,
                'warning': 3,
            },
        }
    },
]


# Security monitoring rules
SECURITY_RULES = [
    {
        'name': 'PHI Exposure Attempt Detected',
        'type': 'log alert',
        'query': 'logs("service:cancer-risk-assessment @warning_flag:phi_detected").index("main").rollup("count").last("5m") > 0',
        'message': '''
**SECURITY ALERT: Potential PHI exposure detected**

System detected attempt to log or transmit Protected Health Information.

**Immediate Actions Required:**
1. Isolate affected systems
2. Review logs for breach confirmation
3. Notify security team and compliance officer
4. Document incident for HIPAA compliance
5. Prepare breach notification if confirmed

This is a critical security event requiring immediate attention.

@security-team
@compliance-team
@pagerduty-security
        '''.strip(),
        'tags': ['service:cancer-risk-assessment', 'priority:critical', 'team:security', 'compliance:hipaa'],
        'priority': 1,
    },
    {
        'name': 'Authentication Failures Spike',
        'type': 'metric alert',
        'query': 'sum(last_10m):sum:cancer_risk.auth.failures{*} > 20',
        'message': '''
Multiple authentication failures detected.

**Possible Causes:**
- Brute force attack
- Misconfigured client
- Expired credentials

**Actions:**
1. Review failed authentication logs
2. Check for IP patterns
3. Consider temporary IP blocking
4. Notify affected users if needed

@security-team
        '''.strip(),
        'tags': ['service:cancer-risk-assessment', 'priority:medium', 'team:security'],
        'priority': 2,
    },
]


# SLO definitions
SLO_DEFINITIONS = [
    {
        'name': 'API Availability',
        'type': 'metric',
        'target': 99.9,
        'query': {
            'numerator': 'sum:cancer_risk.api.requests{status:ok}.as_count()',
            'denominator': 'sum:cancer_risk.api.requests{*}.as_count()',
        },
        'description': '99.9% of API requests should succeed',
    },
    {
        'name': 'Response Time SLO',
        'type': 'metric',
        'target': 99.5,
        'query': {
            'numerator': 'sum:cancer_risk.api.requests{response_time_ms:<2000}.as_count()',
            'denominator': 'sum:cancer_risk.api.requests{*}.as_count()',
        },
        'description': '99.5% of requests should complete in <2 seconds',
    },
    {
        'name': 'Model Confidence SLO',
        'type': 'metric',
        'target': 95.0,
        'query': {
            'numerator': 'sum:cancer_risk.predictions{confidence:>0.7}.as_count()',
            'denominator': 'sum:cancer_risk.predictions{*}.as_count()',
        },
        'description': '95% of predictions should have >70% confidence',
    },
]
