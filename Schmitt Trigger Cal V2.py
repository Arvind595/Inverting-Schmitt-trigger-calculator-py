## Python Calculator: Schmitt Trigger (non-inverting reference form)
#
# Circuit: Vref --R2--+-- R1 -- GND
#                     |
#                     +-- (+) input, R3 feedback from Vout, Vin on (-) input
#
# V_UT = R123 * (Vref/R2 + Voh/R3)
# V_LT = R123 * (Vref/R2 + Vol/R3)
# R123 = R1 || R2 || R3

def schmitt_trigger_resistors(V_UT, hysteresis, V_ref=5.0, Voh=5.0, Vol=-5.0, R123=10000.0):
    if hysteresis <= 0:
        raise ValueError("Hysteresis must be positive.")
    if Voh <= Vol:
        raise ValueError("Output high voltage must be greater than output low voltage.")

    V_LT = V_UT - hysteresis

    # Hysteresis = R123 * (Voh - Vol) / R3
    b = hysteresis / (Voh - Vol)          # b = R123 / R3
    R3 = R123 / b

    # Vref term: a = R123 * Vref / R2 = V_UT - b * Voh
    a = V_UT - b * Voh
    if a <= 0:
        raise ValueError("Thresholds not reachable with this Vref/output swing (R2 would be negative).")
    R2 = R123 * V_ref / a

    # 1/R123 = 1/R1 + 1/R2 + 1/R3
    inv_R1 = (1 / R123) - (1 / R2) - (1 / R3)
    if inv_R1 <= 0:
        raise ValueError("Invalid combination of V_UT, hysteresis and R123. Try a smaller R123.")
    R1 = 1 / inv_R1

    return R1, R2, R3, V_LT


def thresholds(R1, R2, R3, V_ref, Voh, Vol):
    """Verification: recompute thresholds from the resistor values."""
    R123 = 1 / (1 / R1 + 1 / R2 + 1 / R3)
    return (R123 * (V_ref / R2 + Voh / R3),
            R123 * (V_ref / R2 + Vol / R3))


print("\nSchmitt Trigger Resistor Calculator\n")

V_UT = float(input("Enter Upper Trigger Voltage V_UT (V): "))
hysteresis = float(input("Enter Hysteresis (V): "))

V_ref_input = input("Enter Reference Voltage V_REF (default 5 V): ")
Voh_input = input("Enter Output High Voltage +Vcc (default 5 V): ")
Vol_input = input("Enter Output Low Voltage (default -Vcc; enter 0 for single supply): ")
R123_input = input("Enter R123 = R1||R2||R3 (default 10000 ohms): ")

V_ref = float(V_ref_input) if V_ref_input else 5.0
Voh = float(Voh_input) if Voh_input else 5.0
Vol = float(Vol_input) if Vol_input else -Voh
R123 = float(R123_input) if R123_input else 10000.0

R1, R2, R3, V_LT = schmitt_trigger_resistors(V_UT, hysteresis, V_ref, Voh, Vol, R123)
chk_UT, chk_LT = thresholds(R1, R2, R3, V_ref, Voh, Vol)

print("\nResults")
print("-------")
print(f"Lower Trigger Voltage (V_LT) = {V_LT:.3f} V")
print(f"R1 = {R1:.2f} Ω")
print(f"R2 = {R2:.2f} Ω")
print(f"R3 = {R3:.2f} Ω")
print(f"\nCheck: V_UT = {chk_UT:.3f} V, V_LT = {chk_LT:.3f} V")
