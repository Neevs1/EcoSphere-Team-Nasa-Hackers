import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import date, timedelta
from app.database.db import SessionLocal
from app.models.category import Category
from app.models.emission_factor import EmissionFactor
from app.models.carbon_transaction import CarbonTransaction
from app.models.csr_activity import CSRActivity
from app.models.employee_participation import EmployeeParticipation
from app.models.challenge import Challenge
from app.models.badge import Badge
from app.models.reward import Reward
from app.models.compliance_issue import ComplianceIssue
from app.models.audit import Audit
from app.models.department_score import DepartmentScore
from app.models.user import User
from app.models.department import Department

def seed_mock_data():
    db = SessionLocal()
    
    # Check if we already have mock data (e.g., badges)
    if db.query(Badge).first():
        print("Mock data already exists.")
        return
        
    users = db.query(User).all()
    departments = db.query(Department).all()
    categories = db.query(Category).all()
    
    if not users or not departments:
        print("Run initial seed first.")
        return
        
    employee = next((u for u in users if u.role == "employee"), users[-1])
    dept_head = next((u for u in users if u.role == "department_head"), users[0])
    sustainability_dept = next((d for d in departments if d.code == "SUST"), departments[0])
    ops_dept = next((d for d in departments if d.code == "OPS"), departments[1])
    
    # Emission Factors
    ef_elec = EmissionFactor(source="EPA 2024", category="Electricity (Grid)", factor=0.45, unit="kWh")
    ef_flight = EmissionFactor(source="DEFRA 2024", category="Commercial Flight", factor=0.15, unit="km")
    db.add_all([ef_elec, ef_flight])
    db.flush()
    
    # Carbon Transactions
    today = date.today()
    transactions = [
        CarbonTransaction(department_id=ops_dept.id, emission_factor_id=ef_elec.id, quantity=1500, co2_calculated=1500 * 0.45, transaction_date=today - timedelta(days=5)),
        CarbonTransaction(department_id=sustainability_dept.id, emission_factor_id=ef_flight.id, quantity=2500, co2_calculated=2500 * 0.15, transaction_date=today - timedelta(days=2)),
    ]
    db.add_all(transactions)
    
    # Badges
    b_eco = Badge(name="Eco Warrior", description="Completed 5 CSR activities.", unlock_rule="5_csr_events", icon_url="https://api.dicebear.com/7.x/icons/svg?icon=leaf&backgroundColor=10b981")
    b_lead = Badge(name="Sustainability Leader", description="Ranked #1 in department.", unlock_rule="rank_1", icon_url="https://api.dicebear.com/7.x/icons/svg?icon=trophy&backgroundColor=f59e0b")
    db.add_all([b_eco, b_lead])
    db.flush()
    
    # Rewards
    r_mug = Reward(name="Reusable Coffee Mug", description="High quality stainless steel mug.", points_required=50, stock=20)
    r_day = Reward(name="Half Day Off", description="Take an afternoon off.", points_required=500, stock=5)
    db.add_all([r_mug, r_day])
    
    # CSR Activities
    csr_tree = CSRActivity(title="Annual Tree Planting", description="Planting trees at the local park.", points=50, evidence_required=True, status="Open", start_date=today - timedelta(days=1), end_date=today + timedelta(days=10))
    csr_clean = CSRActivity(title="Beach Cleanup", description="Saturday morning beach cleanup.", points=30, evidence_required=False, status="Open")
    db.add_all([csr_tree, csr_clean])
    db.flush()
    
    # Participations
    p_tree = EmployeeParticipation(employee_id=employee.id, activity_id=csr_tree.id, approval_status="Pending", proof_url="https://example.com/proof.jpg")
    p_clean = EmployeeParticipation(employee_id=employee.id, activity_id=csr_clean.id, approval_status="Approved", points_earned=30, completion_date=today - timedelta(days=2))
    db.add_all([p_tree, p_clean])
    
    # Add some points to the user
    employee.points_balance = 120
    employee.xp_total = 120
    
    # Challenges
    chal_bike = Challenge(title="Bike to Work Month", description="Commute by bike for a month.", xp=100, status="Active", deadline=today + timedelta(days=15))
    db.add(chal_bike)
    
    # Audits & Compliance
    audit_q1 = Audit(title="Q1 Sustainability Audit", department_id=ops_dept.id, auditor_id=dept_head.id, findings_summary="Minor issues found.", status="Completed", audit_date=today - timedelta(days=30))
    db.add(audit_q1)
    db.flush()
    
    issue_water = ComplianceIssue(audit_id=audit_q1.id, department_id=ops_dept.id, description="Water usage exceeds limit.", severity="High", status="Open", due_date=today - timedelta(days=2), owner_id=dept_head.id)
    db.add(issue_water)
    
    # Department Scores
    score_ops = DepartmentScore(department_id=ops_dept.id, environmental_score=65, social_score=70, governance_score=80, total_score=71, period="2024-Q1")
    score_sust = DepartmentScore(department_id=sustainability_dept.id, environmental_score=95, social_score=90, governance_score=85, total_score=90, period="2024-Q1")
    db.add_all([score_ops, score_sust])
    
    db.commit()
    print("Mock data seeded successfully!")

if __name__ == "__main__":
    seed_mock_data()
