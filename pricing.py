import pandas as pd
import numpy as np
import QuantLib as ql

# Load parameters 
with open("corporate_finance/parameters_estimation_unity.py") as f: exec(f.read())

# Define the types of real options to evaluate
options = ["Delay", "Expansion", "Abandonment"]

# Loop through each real option
for i in options:
    real_option = i

    # --- QuantLib Setup ---
    # Set the valuation date
    calculation_date = ql.Date(1, 1, 2025)
    ql.Settings.instance().evaluationDate = calculation_date
    # Define the calendar
    calendar = ql.UnitedStates(ql.UnitedStates.NYSE)

    # Set the initial asset price (Enterprise Value, ev)
    initial_price = ql.QuoteHandle(ql.SimpleQuote(ev))

    # Adjust initial price specifically for the Expansion option
    if real_option == "Expansion":
        # Use the synergy value as the initial price for Expansion option
        synergy = 8441.120309
        initial_price = ql.QuoteHandle(ql.SimpleQuote(synergy))

    # Define the day count convention
    day_count = ql.Actual365Fixed()

    # Create a flat risk-free rate term structure
    risk_free_ts = ql.YieldTermStructureHandle(
        ql.FlatForward(calculation_date, risk_free_rate, day_count)
    )

    # Create a flat volatility term structure
    vol_ts = ql.BlackVolTermStructureHandle(
        ql.BlackConstantVol(calculation_date, calendar, volatility, day_count)
    )

    # Define the stochastic process (Black-Scholes in this case)
    process = ql.BlackScholesProcess(initial_price, risk_free_ts, vol_ts)

    # --- Define Option Specifics ---
    # Set strike, maturity, and exercise type based on the option
    if real_option == "Abandonment":
        strike = 3853.31 # Liquidation value or sale price
        maturity_date = ql.Date(31, 12, 2029) # End of option window
        payoff = ql.PlainVanillaPayoff(ql.Option.Put, strike) # Abandonment is a put option

        # Define the American exercise period
        early_exercise_start_date = ql.Date(1, 1, 2027)
        exercise = ql.AmericanExercise(early_exercise_start_date, maturity_date, False)

    elif real_option == "Expansion":
        strike = 13852.78 # Cost to implement expansion
        maturity_date = ql.Date(31, 12, 2026) # Deadline for starting expansion
        payoff = ql.PlainVanillaPayoff(ql.Option.Call, strike) # Expansion is a call option

        # Define the American exercise period
        early_exercise_start_date = ql.Date(1, 1, 2026) # Can expand after one year of assessment
        exercise = ql.AmericanExercise(early_exercise_start_date, maturity_date, False)

    elif real_option == "Delay":
        strike = 18913.21823 # PV of investment cost if the acquisition is made in 2026
        maturity_date = ql.Date(31, 12, 2025) # Deadline to invest
        payoff = ql.PlainVanillaPayoff(ql.Option.Call, strike) # Option to delay is a call option

        # Define the American exercise period
        early_exercise_start_date = ql.Date(1, 1, 2025) # Can start immediately
        exercise = ql.AmericanExercise(early_exercise_start_date, maturity_date, False)

    # Create the option instrument
    option = ql.VanillaOption(payoff, exercise)

    # --- Pricing Engine ---
    # Use a Binomial pricing engine
    binomial_engine = ql.BinomialVanillaEngine(process, "CoxRossRubinstein", 500)

    # Attach the pricing engine to the option
    option.setPricingEngine(binomial_engine)

    # --- Result ---
    # Calculate and print the option price (Net Present Value)
    price = option.NPV()
    print(f"{real_option} American Option Price (Binomial): {price}")