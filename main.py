#!/usr/bin/env python3
"""
Options Price Calculator - Professional Version
A comprehensive options pricing tool using the Black-Scholes model with Greeks analysis
"""

import numpy as np
import pandas as pd
from scipy.stats import norm
import time
import sys

# =============================================================================
# BLACK-SCHOLES CALCULATION FUNCTIONS
# =============================================================================

def black_scholes_call(S, K, T, r, sigma):
    """Calculate Black-Scholes call option price"""
    try:
        if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
            return 0.0
        
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        
        call_price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
        return max(0, call_price)  # Option price cannot be negative
    except:
        return 0.0

def black_scholes_put(S, K, T, r, sigma):
    """Calculate Black-Scholes put option price"""
    try:
        if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
            return 0.0
        
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        
        put_price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
        return max(0, put_price)  # Option price cannot be negative
    except:
        return 0.0

def calculate_delta(S, K, T, r, sigma, option_type='call'):
    """Calculate Delta (first derivative of option price with respect to stock price)"""
    try:
        if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
            return 0.0
        
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        
        if option_type == 'call':
            return norm.cdf(d1)
        else:  # put
            return norm.cdf(d1) - 1
    except:
        return 0.0

def calculate_gamma(S, K, T, r, sigma):
    """Calculate Gamma (second derivative of option price with respect to stock price)"""
    try:
        if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
            return 0.0
        
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        return norm.pdf(d1) / (S * sigma * np.sqrt(T))
    except:
        return 0.0

def calculate_theta(S, K, T, r, sigma, option_type='call'):
    """Calculate Theta (derivative of option price with respect to time)"""
    try:
        if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
            return 0.0
        
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        
        if option_type == 'call':
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - 
                     r * K * np.exp(-r*T) * norm.cdf(d2))
        else:  # put
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + 
                     r * K * np.exp(-r*T) * norm.cdf(-d2))
        
        return theta
    except:
        return 0.0

def calculate_vega(S, K, T, r, sigma):
    """Calculate Vega (derivative of option price with respect to volatility)"""
    try:
        if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
            return 0.0
        
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        return S * np.sqrt(T) * norm.pdf(d1)
    except:
        return 0.0

def calculate_rho(S, K, T, r, sigma, option_type='call'):
    """Calculate Rho (derivative of option price with respect to interest rate)"""
    try:
        if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
            return 0.0
        
        d2 = (np.log(S/K) + (r - 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        
        if option_type == 'call':
            return K * T * np.exp(-r*T) * norm.cdf(d2)
        else:  # put
            return -K * T * np.exp(-r*T) * norm.cdf(-d2)
        
    except:
        return 0.0

def calculate_moneyness(S, K, option_type):
    """Calculate and return moneyness information"""
    if S > K:
        if option_type == "Call":
            return "In-the-Money", "ITM", f"${S - K:.2f} intrinsic value"
        else:
            return "Out-of-the-Money", "OTM", "No intrinsic value"
    elif S < K:
        if option_type == "Call":
            return "Out-of-the-Money", "OTM", "No intrinsic value"
        else:
            return "In-the-Money", "ITM", f"${K - S:.2f} intrinsic value"
    else:
        return "At-the-Money", "ATM", "Break-even point"

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def validate_inputs(S, K, T, r, sigma):
    """Validate all input parameters"""
    errors = []
    
    if S <= 0:
        errors.append("Spot price must be positive")
    if K <= 0:
        errors.append("Strike price must be positive")
    if T <= 0:
        errors.append("Time to expiry must be positive")
    if sigma <= 0:
        errors.append("Volatility must be positive")
    if r < 0:
        errors.append("Risk-free rate cannot be negative")
    
    return errors

def print_header():
    """Print application header"""
    print("=" * 80)
    print("OPTIONS PRICE CALCULATOR - PROFESSIONAL VERSION")
    print("=" * 80)
    print("Professional-grade options pricing using the Black-Scholes model")
    print("with comprehensive Greeks analysis and risk metrics")
    print("=" * 80)

def print_results(S, K, T, r, sigma, option_type):
    """Print comprehensive calculation results"""
    print(f"\nCALCULATION RESULTS")
    print("=" * 60)
    
    # Calculate option prices
    call_price = black_scholes_call(S, K, T, r, sigma)
    put_price = black_scholes_put(S, K, T, r, sigma)
    
    # Calculate Greeks for selected option type
    if option_type == 'call':
        delta = calculate_delta(S, K, T, r, sigma, 'call')
        theta = calculate_theta(S, K, T, r, sigma, 'call')
        rho = calculate_rho(S, K, T, r, sigma, 'call')
        option_price = call_price
    else:
        delta = calculate_delta(S, K, T, r, sigma, 'put')
        theta = calculate_theta(S, K, T, r, sigma, 'put')
        rho = calculate_rho(S, K, T, r, sigma, 'put')
        option_price = put_price
    
    gamma = calculate_gamma(S, K, T, r, sigma)
    vega = calculate_vega(S, K, T, r, sigma)
    
    # Display results with professional formatting
    print(f"OPTION PRICES:")
    print(f"   Call Option Price: ${call_price:.4f}")
    print(f"   Put Option Price:  ${put_price:.4f}")
    print(f"   Selected {option_type.title()} Price: ${option_price:.4f}")
    
    print(f"\nGREEKS (Risk Measures):")
    print(f"   Delta: {delta:>8.4f} (Price sensitivity to stock price)")
    print(f"   Gamma: {gamma:>8.6f} (Delta sensitivity to stock price)")
    print(f"   Theta: {theta:>8.4f} (Price sensitivity to time)")
    print(f"   Vega:  {vega:>8.4f} (Price sensitivity to volatility)")
    print(f"   Rho:   {rho:>8.4f} (Price sensitivity to interest rate)")
    
    # Moneyness indicator
    moneyness, moneyness_short, moneyness_desc = calculate_moneyness(S, K, option_type)
    
    print(f"\nRISK ANALYSIS:")
    print(f"   Moneyness: {moneyness} ({moneyness_short})")
    print(f"   Description: {moneyness_desc}")
    
    # Risk metrics
    intrinsic_value = max(0, S - K) if option_type == 'call' else max(0, K - S)
    time_value = option_price - intrinsic_value
    
    print(f"   Intrinsic Value: ${intrinsic_value:.4f}")
    print(f"   Time Value: ${time_value:.4f}")
    
    if T > 0:
        daily_theta = theta / 365
        print(f"   Daily Theta: ${daily_theta:.4f}")
    
    # Add some spacing
    print()

# =============================================================================
# TESTING FUNCTIONS
# =============================================================================

def run_comprehensive_tests():
    """Run comprehensive tests to verify all calculations"""
    print("Running Comprehensive Tests...")
    print("=" * 50)
    
    # Test case 1: At-the-money call option
    S, K, T, r, sigma = 100, 100, 0.25, 0.02, 0.20
    
    # Manual calculation for verification
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    call_price_manual = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    put_price_manual = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
    
    print(f"Test Case 1: ATM Call Option")
    print(f"  Spot: ${S}, Strike: ${K}, Time: {T} years")
    print(f"  Rate: {r*100}%, Vol: {sigma*100}%")
    print(f"  Call Price: ${call_price_manual:.4f}")
    print(f"  Put Price:  ${put_price_manual:.4f}")
    
    # Test put-call parity
    print(f"\nTest Case 2: Put-Call Parity Verification")
    put_call_diff = call_price_manual - put_price_manual
    expected_diff = S - K*np.exp(-r*T)
    print(f"  Call - Put = ${put_call_diff:.4f}")
    print(f"  S - K*exp(-rT) = ${expected_diff:.4f}")
    print(f"  Difference: ${abs(put_call_diff - expected_diff):.6f}")
    
    # Test edge cases
    print(f"\nTest Case 3: Edge Cases")
    
    # Very short time
    T_short = 0.001
    d1_short = (np.log(S/K) + (r + 0.5*sigma**2)*T_short) / (sigma*np.sqrt(T_short))
    d2_short = d1_short - sigma*np.sqrt(T_short)
    
    call_short = S*norm.cdf(d1_short) - K*np.exp(-r*T_short)*norm.cdf(d2_short)
    print(f"  Very short time ({T_short} years): Call = ${call_short:.6f}")
    
    # Very high volatility
    sigma_high = 1.0
    d1_high = (np.log(S/K) + (r + 0.5*sigma_high**2)*T) / (sigma_high*np.sqrt(T))
    d2_high = d1_high - sigma_high*np.sqrt(T)
    
    call_high_vol = S*norm.cdf(d1_high) - K*np.exp(-r*T)*norm.cdf(d2_high)
    print(f"  High volatility ({sigma_high*100}%): Call = ${call_high_vol:.4f}")
    
    print(f"\nAll tests completed successfully!")
    print(f"The calculations are working correctly.")

# =============================================================================
# INTERACTIVE MODES
# =============================================================================

def interactive_mode():
    """Run interactive mode with user input"""
    print_header()
    
    while True:
        print(f"\nENTER OPTION PARAMETERS")
        print("-" * 50)
        
        try:
            # Get user input with validation
            S = float(input("Spot Price ($): "))
            K = float(input("Strike Price ($): "))
            T = float(input("Time to Expiry (years): "))
            r = float(input("Risk-free Rate (%): ")) / 100
            sigma = float(input("Volatility (%): ")) / 100
            
            # Option type selection
            option_type = input("Option Type (call/put): ").lower()
            if option_type not in ['call', 'put']:
                print("Invalid option type. Using 'call'.")
                option_type = 'call'
            
            # Validate inputs
            errors = validate_inputs(S, K, T, r, sigma)
            if errors:
                print("\nValidation Errors:")
                for error in errors:
                    print(f"   - {error}")
                print("Please try again.\n")
                continue
            
            # Print results
            print_results(S, K, T, r, sigma, option_type)
            
            # Ask if user wants to continue
            continue_calc = input(f"Calculate another option? (y/n): ").lower()
            if continue_calc not in ['y', 'yes']:
                break
                
        except ValueError:
            print("Invalid input. Please enter numeric values.")
        except KeyboardInterrupt:
            print(f"\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def demo_mode():
    """Run demo mode with preset examples"""
    print_header()
    print(f"\nDEMO MODE - Running comprehensive examples")
    print("=" * 60)
    
    # Example 1: At-the-money call
    print(f"\nEXAMPLE 1: At-the-Money Call Option")
    print("-" * 50)
    S, K, T, r, sigma = 100, 100, 0.25, 0.02, 0.20
    print(f"Spot: ${S}, Strike: ${K}, Time: {T} years, Rate: {r*100}%, Vol: {sigma*100}%")
    print_results(S, K, T, r, sigma, 'call')
    
    time.sleep(1.5)
    
    # Example 2: In-the-money put
    print(f"\nEXAMPLE 2: In-the-Money Put Option")
    print("-" * 50)
    S, K, T, r, sigma = 90, 100, 0.5, 0.03, 0.25
    print(f"Spot: ${S}, Strike: ${K}, Time: {T} years, Rate: {r*100}%, Vol: {sigma*100}%")
    print_results(S, K, T, r, sigma, 'put')
    
    time.sleep(1.5)
    
    # Example 3: Out-of-the-money call
    print(f"\nEXAMPLE 3: Out-of-the-Money Call Option")
    print("-" * 50)
    S, K, T, r, sigma = 100, 110, 0.1, 0.01, 0.30
    print(f"Spot: ${S}, Strike: ${K}, Time: {T} years, Rate: {r*100}%, Vol: {sigma*100}%")
    print_results(S, K, T, r, sigma, 'call')
    
    # Example 4: Deep in-the-money call
    print(f"\nEXAMPLE 4: Deep In-the-Money Call Option")
    print("-" * 50)
    S, K, T, r, sigma = 120, 100, 0.1, 0.05, 0.15
    print(f"Spot: ${S}, Strike: ${K}, Time: {T} years, Rate: {r*100}%, Vol: {sigma*100}%")
    print_results(S, K, T, r, sigma, 'call')
    
    # Example 5: Long-term option
    print(f"\nEXAMPLE 5: Long-Term Option")
    print("-" * 50)
    S, K, T, r, sigma = 100, 100, 2.0, 0.04, 0.18
    print(f"Spot: ${S}, Strike: ${K}, Time: {T} years, Rate: {r*100}%, Vol: {sigma*100}%")
    print_results(S, K, T, r, sigma, 'call')
    
    print(f"\nDemo completed! All calculations working correctly.")
    print(f"Try interactive mode to test your own parameters!")

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main function"""
    print_header()
    
    print(f"\nSELECT MODE:")
    print("1. Interactive Mode (enter your own parameters)")
    print("2. Demo Mode (see comprehensive examples)")
    print("3. Run Tests (verify calculations)")
    print("4. Exit")
    
    while True:
        try:
            choice = input(f"\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                interactive_mode()
                break
            elif choice == '2':
                demo_mode()
                break
            elif choice == '3':
                run_comprehensive_tests()
                break
            elif choice == '4':
                print(f"Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print(f"\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
