import math
from datetime import datetime
from typing import Dict, Any

def calculate_legal_interest(principal: float, rate: float, days: int) -> Dict[str, Any]:
    """
    Calculates Simple and Compound Legal Interest under Section 34 CPC.
    """
    simple_interest = (principal * rate * days) / (365 * 100)
    total_simple = principal + simple_interest
    
    # Compound annual interest
    years = days / 365.0
    compound_total = principal * math.pow((1 + (rate / 100.0)), years)
    compound_interest = compound_total - principal

    return {
        "principal": principal,
        "rate": rate,
        "days": days,
        "simple_interest": round(simple_interest, 2),
        "total_simple": round(total_simple, 2),
        "compound_interest": round(compound_interest, 2),
        "total_compound": round(compound_total, 2)
    }


def calculate_limitation_period(start_date_str: str, cause_type: str = "Contract Breach") -> Dict[str, Any]:
    """
    Calculates Limitation Period expiry under Indian Limitation Act, 1963.
    """
    limitation_years_map = {
        "Contract Breach": 3,
        "Recovery of Money": 3,
        "Cheque Dishonor (Sec 138)": 0.08, # 30 days
        "Property Possession (Mortgage)": 12,
        "Appeal to High Court": 0.25, # 90 days
        "Tort & Personal Injury": 1
    }

    years = limitation_years_map.get(cause_type, 3)
    try:
        dt = datetime.strptime(start_date_str, "%Y-%m-%d")
        if years < 1:
            expiry_days = int(years * 365)
            from datetime import timedelta
            expiry_dt = dt + timedelta(days=expiry_days)
        else:
            expiry_dt = datetime(dt.year + int(years), dt.month, dt.day)

        days_remaining = (expiry_dt - datetime.now()).days

        return {
            "start_date": start_date_str,
            "cause_type": cause_type,
            "limitation_period_years": years,
            "expiry_date": expiry_dt.strftime("%B %d, %Y"),
            "days_remaining": days_remaining,
            "is_expired": days_remaining < 0
        }
    except Exception as e:
        return {
            "error": f"Invalid date format: {e}. Please use YYYY-MM-DD."
        }


def estimate_stamp_duty(amount: float, doc_type: str = "Sale Agreement", state: str = "Maharashtra") -> Dict[str, Any]:
    """
    Estimates Stamp Duty & Registration Fees across major states.
    """
    rates = {
        "Sale Agreement": 0.05,
        "Rental Agreement": 0.0025,
        "Mortgage Deed": 0.005,
        "Power of Attorney": 0.01,
        "General Contract": 0.001
    }
    rate = rates.get(doc_type, 0.005)
    stamp_duty = amount * rate
    registration_fee = min(30000.0, max(1000.0, amount * 0.01))

    return {
        "amount": amount,
        "doc_type": doc_type,
        "state": state,
        "stamp_duty_rate": f"{rate * 100}%",
        "estimated_stamp_duty": round(stamp_duty, 2),
        "estimated_registration_fee": round(registration_fee, 2),
        "total_cost": round(stamp_duty + registration_fee, 2)
    }
