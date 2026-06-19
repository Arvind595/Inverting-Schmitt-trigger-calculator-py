## ?? Python Calculator

def schmitt_trigger_resistors(V_UT, hysteresis, V_ref=5.0, Vcc=5.0, R123=10000):
    V_LT = V_UT - hysteresis

    # Calculate R3 and R2
    R3 = R123 / ((V_UT - V_LT) / Vcc)
    R2 = R123 / (V_LT / V_ref)

    # Calculate R1 using parallel resistance formula
    inv_R1 = (1 / R123) - (1 / R2) - (1 / R3)

    if inv_R1 <= 0:
        raise ValueError(
            "Invalid combination of V_UT, hysteresis and R123."
        )

    R1 = 1 / inv_R1

    return R1, R2, R3


print("\nSchmitt Trigger Resistor Calculator\n")

V_UT = float(input("Enter Upper Trigger Voltage V_UT (V): "))
hysteresis = float(input("Enter Hysteresis (V): "))

V_ref_input = input("Enter Reference Voltage V_REF (default 5V): ")
Vcc_input = input("Enter Output High Voltage VCC (default 5V): ")
R123_input = input("Enter R123 = R1||R2||R3 (default 10000 ohms): ")

V_ref = float(V_ref_input) if V_ref_input else 5.0
Vcc = float(Vcc_input) if Vcc_input else 5.0
R123 = float(R123_input) if R123_input else 10000.0

R1, R2, R3 = schmitt_trigger_resistors(
    V_UT,
    hysteresis,
    V_ref,
    Vcc,
    R123
)

print("\nResults")
print("-------")
print(f"Lower Trigger Voltage (V_LT) = {V_UT - hysteresis:.3f} V")
print(f"R1 = {R1:.2f} O")
print(f"R2 = {R2:.2f} O")
print(f"R3 = {R3:.2f} O")