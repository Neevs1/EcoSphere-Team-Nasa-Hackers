from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud import (
    department_crud,
    category_crud,
    emission_factor_crud,
    product_esg_profile_crud,
    environmental_goal_crud,
    esg_policy_crud,
    badge_crud,
    reward_crud,
    carbon_transaction_crud,
    csr_activity_crud,
    employee_participation_crud,
    challenge_crud,
    challenge_participation_crud,
    policy_acknowledgement_crud,
    audit_crud,
    compliance_issue_crud,
    department_score_crud,
)

from app.models import ComplianceIssue

from app.schemas import (
    CarbonTransactionCreate,
    ChallengeParticipationCreate,
    DepartmentScoreCreate,
    EmployeeParticipationCreate,
)

from app.services.base import BaseService


# =========================================================
# GENERIC SERVICES
# =========================================================

department_service = BaseService(department_crud)
category_service = BaseService(category_crud)
emission_factor_service = BaseService(emission_factor_crud)
product_esg_profile_service = BaseService(
    product_esg_profile_crud
)
environmental_goal_service = BaseService(
    environmental_goal_crud
)
esg_policy_service = BaseService(esg_policy_crud)
badge_service = BaseService(badge_crud)
reward_service = BaseService(reward_crud)
csr_activity_service = BaseService(csr_activity_crud)
employee_participation_service = BaseService(
    employee_participation_crud
)
challenge_service = BaseService(challenge_crud)
challenge_participation_service = BaseService(
    challenge_participation_crud
)
policy_acknowledgement_service = BaseService(
    policy_acknowledgement_crud
)
audit_service = BaseService(audit_crud)
compliance_issue_service = BaseService(
    compliance_issue_crud
)
department_score_service = BaseService(
    department_score_crud
)


#CARBON SERVICE

class CarbonService:
    """
    Business logic for automatic carbon emission calculation.

    Formula:
        emission = quantity × emission factor
    """

    def create_transaction(
        self,
        db: Session,
        obj_in: CarbonTransactionCreate,
    ):
        department = department_crud.get(
            db,
            obj_in.department_id,
        )

        if department is None:
            raise ValueError(
                "Department does not exist."
            )

        emission_factor = emission_factor_crud.get(
            db,
            obj_in.emission_factor_id,
        )

        if emission_factor is None:
            raise ValueError(
                "Emission factor does not exist."
            )

        if not emission_factor.status:
            raise ValueError(
                "Selected emission factor is inactive."
            )

        if obj_in.product_profile_id is not None:
            product = product_esg_profile_crud.get(
                db,
                obj_in.product_profile_id,
            )

            if product is None:
                raise ValueError(
                    "Product ESG profile does not exist."
                )

        calculated_emission = round(
            obj_in.quantity * emission_factor.factor,
            4,
        )

        transaction_data = obj_in.model_copy(
            update={
                "emission": calculated_emission,
            }
        )

        return carbon_transaction_crud.create(
            db,
            obj_in=transaction_data,
        )


carbon_service = CarbonService()


#DEPARTMENT ESG SERVICE
class DepartmentESGScoreService:
    """
    Default EcoSphere weighting:

    Environmental: 40%
    Social: 30%
    Governance: 30%
    """

    ENVIRONMENTAL_WEIGHT = 0.40
    SOCIAL_WEIGHT = 0.30
    GOVERNANCE_WEIGHT = 0.30

    def calculate_total(
        self,
        environmental_score: float,
        social_score: float,
        governance_score: float,
    ) -> float:
        scores = (
            environmental_score,
            social_score,
            governance_score,
        )

        if any(
            score < 0 or score > 100
            for score in scores
        ):
            raise ValueError(
                "All ESG scores must be between 0 and 100."
            )

        total = (
            environmental_score
            * self.ENVIRONMENTAL_WEIGHT
            + social_score
            * self.SOCIAL_WEIGHT
            + governance_score
            * self.GOVERNANCE_WEIGHT
        )

        return round(total, 2)

    def create_score(
        self,
        db: Session,
        obj_in: DepartmentScoreCreate,
    ):
        department = department_crud.get(
            db,
            obj_in.department_id,
        )

        if department is None:
            raise ValueError(
                "Department does not exist."
            )

        total = self.calculate_total(
            environmental_score=(
                obj_in.environmental_score
            ),
            social_score=obj_in.social_score,
            governance_score=(
                obj_in.governance_score
            ),
        )

        score_data = obj_in.model_copy(
            update={
                "total_score": total,
            }
        )

        return department_score_crud.create(
            db,
            obj_in=score_data,
        )


department_esg_score_service = (
    DepartmentESGScoreService()
)


#CSR PARTICIPATION SERVICE
class CSRParticipationService:
    """
    Validates CSR activity participation.
    """

    def create_participation(
        self,
        db: Session,
        obj_in: EmployeeParticipationCreate,
        *,
        evidence_required: bool = False,
    ):
        activity = csr_activity_crud.get(
            db,
            obj_in.csr_activity_id,
        )

        if activity is None:
            raise ValueError(
                "CSR activity does not exist."
            )

        if evidence_required and not obj_in.proof:
            raise ValueError(
                "Proof is required for this CSR participation."
            )

        return employee_participation_crud.create(
            db,
            obj_in=obj_in,
        )


csr_participation_service = CSRParticipationService()


#CHALLENGE PARTICIPATION

class ChallengeParticipationBusinessService:
    """
    Validates challenge participation and XP awarding.
    """

    def create_participation(
        self,
        db: Session,
        obj_in: ChallengeParticipationCreate,
    ):
        challenge = challenge_crud.get(
            db,
            obj_in.challenge_id,
        )

        if challenge is None:
            raise ValueError(
                "Challenge does not exist."
            )

        if challenge.status not in {
            "Active",
            "Under Review",
        }:
            raise ValueError(
                "Employees can only participate "
                "in active challenges."
            )

        if (
            challenge.evidence_required
            and obj_in.progress == 100
            and not obj_in.proof
        ):
            raise ValueError(
                "Proof is required to complete this challenge."
            )

        xp_awarded = 0

        if (
            obj_in.progress == 100
            and obj_in.approval == "Approved"
        ):
            xp_awarded = challenge.xp or 0

        participation_data = obj_in.model_copy(
            update={
                "xp_awarded": xp_awarded,
            }
        )

        return challenge_participation_crud.create(
            db,
            obj_in=participation_data,
        )


challenge_participation_business_service = (
    ChallengeParticipationBusinessService()
)


#COMPLIANCE SERVICE

class ComplianceService:
    """
    Finds overdue open compliance issues.
    """

    def get_overdue_issues(
        self,
        db: Session,
    ) -> list[ComplianceIssue]:
        statement = select(
            ComplianceIssue
        ).where(
            ComplianceIssue.due_date < date.today(),
            ComplianceIssue.status.in_(
                [
                    "Open",
                    "Pending",
                    "In Progress",
                ]
            ),
        )

        return list(
            db.scalars(statement).all()
        )


compliance_service = ComplianceService()


#REWARD SERVICE
class RewardBusinessService:
    """
    Validates reward redemption conditions.

    Your current database does not yet contain an Employee
    points balance or RewardRedemption table, so this service
    currently validates the redemption and reduces stock.
    """

    def validate_redemption(
        self,
        db: Session,
        *,
        reward_id: int,
        employee_points: int,
    ) -> dict:
        reward = reward_crud.get(
            db,
            reward_id,
        )

        if reward is None:
            raise ValueError(
                "Reward does not exist."
            )

        if not reward.status:
            raise ValueError(
                "Reward is inactive."
            )

        if reward.stock <= 0:
            raise ValueError(
                "Reward is out of stock."
            )

        if employee_points < reward.points_required:
            raise ValueError(
                "Employee does not have enough points."
            )

        return {
            "reward": reward,
            "remaining_points": (
                employee_points
                - reward.points_required
            ),
        }

    def reduce_stock(
        self,
        db: Session,
        *,
        reward_id: int,
    ):
        reward = reward_crud.get(
            db,
            reward_id,
        )

        if reward is None:
            raise ValueError(
                "Reward does not exist."
            )

        if reward.stock <= 0:
            raise ValueError(
                "Reward is out of stock."
            )

        return reward_crud.update(
            db,
            db_object=reward,
            obj_in={
                "stock": reward.stock - 1,
            },
        )


reward_business_service = RewardBusinessService()