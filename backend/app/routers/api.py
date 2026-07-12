from fastapi import APIRouter

from app.routers.base import create_crud_router

from app.schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    EmissionFactorCreate,
    EmissionFactorUpdate,
    EmissionFactorResponse,
    ProductESGProfileCreate,
    ProductESGProfileUpdate,
    ProductESGProfileResponse,
    EnvironmentalGoalCreate,
    EnvironmentalGoalUpdate,
    EnvironmentalGoalResponse,
    ESGPolicyCreate,
    ESGPolicyUpdate,
    ESGPolicyResponse,
    BadgeCreate,
    BadgeUpdate,
    BadgeResponse,
    RewardCreate,
    RewardUpdate,
    RewardResponse,
    CarbonTransactionCreate,
    CarbonTransactionUpdate,
    CarbonTransactionResponse,
    CSRActivityCreate,
    CSRActivityUpdate,
    CSRActivityResponse,
    EmployeeParticipationCreate,
    EmployeeParticipationUpdate,
    EmployeeParticipationResponse,
    ChallengeCreate,
    ChallengeUpdate,
    ChallengeResponse,
    ChallengeParticipationCreate,
    ChallengeParticipationUpdate,
    ChallengeParticipationResponse,
    PolicyAcknowledgementCreate,
    PolicyAcknowledgementUpdate,
    PolicyAcknowledgementResponse,
    AuditCreate,
    AuditUpdate,
    AuditResponse,
    ComplianceIssueCreate,
    ComplianceIssueUpdate,
    ComplianceIssueResponse,
    DepartmentScoreCreate,
    DepartmentScoreUpdate,
    DepartmentScoreResponse,
)

from app.services import (
    department_service,
    category_service,
    emission_factor_service,
    product_esg_profile_service,
    environmental_goal_service,
    esg_policy_service,
    badge_service,
    reward_service,
    carbon_transaction_service,
    csr_activity_service,
    employee_participation_service,
    challenge_service,
    challenge_participation_service,
    policy_acknowledgement_service,
    audit_service,
    compliance_issue_service,
    department_score_service,
)


api_router = APIRouter()



#master routers

department_router = create_crud_router(
    service=department_service,
    create_schema=DepartmentCreate,
    update_schema=DepartmentUpdate,
    response_schema=DepartmentResponse,
    prefix="/departments",
    tag="Departments",
    resource_name="Department",
    write_roles=["system_admin", "esg_admin"],
)

category_router = create_crud_router(
    service=category_service,
    create_schema=CategoryCreate,
    update_schema=CategoryUpdate,
    response_schema=CategoryResponse,
    prefix="/categories",
    tag="Categories",
    resource_name="Category",
    write_roles=["system_admin", "esg_admin"],
)

emission_factor_router = create_crud_router(
    service=emission_factor_service,
    create_schema=EmissionFactorCreate,
    update_schema=EmissionFactorUpdate,
    response_schema=EmissionFactorResponse,
    prefix="/emission-factors",
    tag="Emission Factors",
    resource_name="Emission factor",
    write_roles=["system_admin", "esg_admin"],
)

product_esg_profile_router = create_crud_router(
    service=product_esg_profile_service,
    create_schema=ProductESGProfileCreate,
    update_schema=ProductESGProfileUpdate,
    response_schema=ProductESGProfileResponse,
    prefix="/product-esg-profiles",
    tag="Product ESG Profiles",
    resource_name="Product ESG profile",
    write_roles=["system_admin", "esg_admin"],
)

environmental_goal_router = create_crud_router(
    service=environmental_goal_service,
    create_schema=EnvironmentalGoalCreate,
    update_schema=EnvironmentalGoalUpdate,
    response_schema=EnvironmentalGoalResponse,
    prefix="/environmental-goals",
    tag="Environmental Goals",
    resource_name="Environmental goal",
    write_roles=["system_admin", "esg_admin"],
)

esg_policy_router = create_crud_router(
    service=esg_policy_service,
    create_schema=ESGPolicyCreate,
    update_schema=ESGPolicyUpdate,
    response_schema=ESGPolicyResponse,
    prefix="/esg-policies",
    tag="ESG Policies",
    resource_name="ESG policy",
    write_roles=["system_admin", "esg_admin"],
)

badge_router = create_crud_router(
    service=badge_service,
    create_schema=BadgeCreate,
    update_schema=BadgeUpdate,
    response_schema=BadgeResponse,
    prefix="/badges",
    tag="Badges",
    resource_name="Badge",
    write_roles=["system_admin", "esg_admin"],
)

reward_router = create_crud_router(
    service=reward_service,
    create_schema=RewardCreate,
    update_schema=RewardUpdate,
    response_schema=RewardResponse,
    prefix="/rewards",
    tag="Rewards",
    resource_name="Reward",
    write_roles=["system_admin", "esg_admin"],
)


#transactional data routers

carbon_transaction_router = create_crud_router(
    service=carbon_transaction_service,
    create_schema=CarbonTransactionCreate,
    update_schema=CarbonTransactionUpdate,
    response_schema=CarbonTransactionResponse,
    prefix="/carbon-transactions",
    tag="Carbon Transactions",
    resource_name="Carbon transaction",
    write_roles=["system_admin", "esg_admin", "department_head"],
)

csr_activity_router = create_crud_router(
    service=csr_activity_service,
    create_schema=CSRActivityCreate,
    update_schema=CSRActivityUpdate,
    response_schema=CSRActivityResponse,
    prefix="/csr-activities",
    tag="CSR Activities",
    resource_name="CSR activity",
    write_roles=["system_admin", "esg_admin", "department_head"],
)

employee_participation_router = create_crud_router(
    service=employee_participation_service,
    create_schema=EmployeeParticipationCreate,
    update_schema=EmployeeParticipationUpdate,
    response_schema=EmployeeParticipationResponse,
    prefix="/employee-participations",
    tag="Employee Participations",
    resource_name="Employee participation",
)

challenge_router = create_crud_router(
    service=challenge_service,
    create_schema=ChallengeCreate,
    update_schema=ChallengeUpdate,
    response_schema=ChallengeResponse,
    prefix="/challenges",
    tag="Challenges",
    resource_name="Challenge",
    write_roles=["system_admin", "esg_admin", "department_head"],
)

challenge_participation_router = create_crud_router(
    service=challenge_participation_service,
    create_schema=ChallengeParticipationCreate,
    update_schema=ChallengeParticipationUpdate,
    response_schema=ChallengeParticipationResponse,
    prefix="/challenge-participations",
    tag="Challenge Participations",
    resource_name="Challenge participation",
)

policy_acknowledgement_router = create_crud_router(
    service=policy_acknowledgement_service,
    create_schema=PolicyAcknowledgementCreate,
    update_schema=PolicyAcknowledgementUpdate,
    response_schema=PolicyAcknowledgementResponse,
    prefix="/policy-acknowledgements",
    tag="Policy Acknowledgements",
    resource_name="Policy acknowledgement",
)

audit_router = create_crud_router(
    service=audit_service,
    create_schema=AuditCreate,
    update_schema=AuditUpdate,
    response_schema=AuditResponse,
    prefix="/audits",
    tag="Audits",
    resource_name="Audit",
    write_roles=["system_admin", "esg_admin", "compliance_officer"],
)

compliance_issue_router = create_crud_router(
    service=compliance_issue_service,
    create_schema=ComplianceIssueCreate,
    update_schema=ComplianceIssueUpdate,
    response_schema=ComplianceIssueResponse,
    prefix="/compliance-issues",
    tag="Compliance Issues",
    resource_name="Compliance issue",
    write_roles=["system_admin", "esg_admin", "compliance_officer"],
)

department_score_router = create_crud_router(
    service=department_score_service,
    create_schema=DepartmentScoreCreate,
    update_schema=DepartmentScoreUpdate,
    response_schema=DepartmentScoreResponse,
    prefix="/department-scores",
    tag="Department Scores",
    resource_name="Department score",
)


# =========================================================
# REGISTER ALL CRUD ROUTERS
# =========================================================

api_router.include_router(department_router)
api_router.include_router(category_router)
api_router.include_router(emission_factor_router)
api_router.include_router(product_esg_profile_router)
api_router.include_router(environmental_goal_router)
api_router.include_router(esg_policy_router)
api_router.include_router(badge_router)
api_router.include_router(reward_router)

api_router.include_router(carbon_transaction_router)
api_router.include_router(csr_activity_router)
api_router.include_router(employee_participation_router)
api_router.include_router(challenge_router)
api_router.include_router(challenge_participation_router)
api_router.include_router(policy_acknowledgement_router)
api_router.include_router(audit_router)
api_router.include_router(compliance_issue_router)
api_router.include_router(department_score_router)