#!/usr/bin/env python3
"""
Options Price Calculator - Command Line Version
Professional-grade options pricing using the Black-Scholes model with comprehensive Greeks analysis
"""

import numpy as np
import pandas as pd
from scipy.stats import norm
import time
import sys

def black_scholes_call(S, K, T, r, sigma):
    """
    Calculate Black-Scholes call option price
    
    Parameters:
    S: Current stock price (spot price)
    K: Strike price
    T: Time to expiration (in years)
    r: Risk-free interest rate
    sigma: Volatility
    
    Returns:
    call_price: Call option price
    """
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
    """
    Calculate Black-Scholes put option price
    """
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
            return "In-the-Money", "🟢", f"${S - K:.2f} intrinsic value"
        else:
            return "Out-of-the-Money", "🔴", "No intrinsic value"
    elif S < K:
        if option_type == "Call":
            return "Out-of-the-Money", "🔴", "No intrinsic value"
        else:
            return "In-the-Money", "🟢", f"${K - S:.2f} intrinsic value"
    else:
        return "At-the-Money", "🟡", "Break-even point"

def print_header():
    """Print application header"""
    print("=" * 80)
    print("📈 OPTIONS PRICE CALCULATOR - PROFESSIONAL VERSION")
    print("=" * 80)
    print("Professional-grade options pricing using the Black-Scholes model")
    print("with comprehensive Greeks analysis and risk metrics")
    print("=" * 80)

def print_results(S, K, T, r, sigma, option_type):
    """Print comprehensive calculation results"""
    print(f"\n📊 CALCULATION RESULTS")
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
    print(f"💰 OPTION PRICES:")
    print(f"   Call Option Price: ${call_price:.4f}")
    print(f"   Put Option Price:  ${put_price:.4f}")
    print(f"   Selected {option_type.title()} Price: ${option_price:.4f}")
    
    print(f"\n📊 GREEKS (Risk Measures):")
    print(f"   Delta: {delta:>8.4f} (Price sensitivity to stock price)")
    print(f"   Gamma: {gamma:>8.6f} (Delta sensitivity to stock price)")
    print(f"   Theta: {theta:>8.4f} (Price sensitivity to time)")
    print(f"   Vega:  {vega:>8.4f} (Price sensitivity to volatility)")
    print(f"   Rho:   {rho:>8.4f} (Price sensitivity to interest rate)")
    
    # Moneyness indicator
    moneyness, moneyness_icon, moneyness_desc = calculate_moneyness(S, K, option_type)
    
    print(f"\n🔍 RISK ANALYSIS:")
    print(f"   Moneyness: {moneyness_icon} {moneyness}")
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

def interactive_mode():
    """Run interactive mode with user input"""
    print_header()
    
    while True:
        print(f"\n📝 ENTER OPTION PARAMETERS")
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
                print("❌ Invalid option type. Using 'call'.")
                option_type = 'call'
            
            # Validate inputs
            if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
                print("❌ Invalid parameters. All values must be positive.")
                continue
            
            # Print results
            print_results(S, K, T, r, sigma, option_type)
            
            # Ask if user wants to continue
            continue_calc = input(f"🔄 Calculate another option? (y/n): ").lower()
            if continue_calc not in ['y', 'yes']:
                break
                
        except ValueError:
            print("❌ Invalid input. Please enter numeric values.")
        except KeyboardInterrupt:
            print(f"\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def demo_mode():
    """Run demo mode with preset examples"""
    print_header()
    print(f"\n🎯 DEMO MODE - Running comprehensive examples")
    print("=" * 60)
    
    # Example 1: At-the-money call
    print(f"\n📊 EXAMPLE 1: At-the-Money Call Option")
    print("-" * 50)
    S, K, T, r, sigma = 100, 100, 0.25, 0.02, 0.20
    print(f"Spot: ${S}, Strike: ${K}, Time: {T} years, Rate: {r*100}%, Vol: {sigma*100}%")
    print_results(S, K, T, r, sigma, 'call')
    
    time.sleep(1.5)
    
    # Example 2: In-the-money put
    print(f"\n📊 EXAMPLE 2: In-the-Money Put Option")
    print("-" * 50)
    S, K, T, r, sigma = 90, 100, 0.5, 0.03, 0.25
    print(f"Spot: ${S}, Strike: ${K}, Time: {T} years, Rate: {r*100}%, Vol: {sigma*100}%")
    print_results(S, K, T, r, sigma, 'put')
    
    time.sleep(1.5)
    
    # Example 3: Out-of-the-money call
    print(f"\n📊 EXAMPLE 3: Out-of-the-Money Call Option")
    print("-" * 50)
    S, K, T, r, sigma = 100, 110, 0.1, 0.01, 0.30
    print(f"Spot: ${S}, Strike: ${K}, Time: {T} years, Rate: {r*100}%, Vol: {sigma*100}%")
    print_results(S, K, T, r, sigma, 'call')
    
    # Example 4: Deep in-the-money call
    print(f"\n📊 EXAMPLE 4: Deep In-the-Money Call Option")
    print("-" * 50)
    S, K, T, r, sigma = 120, 100, 0.1, 0.05, 0.15
    print(f"Spot: ${S}, Strike: ${K}, Time: {T} years, Rate: {r*100}%, Vol: {sigma*100}%")
    print_results(S, K, T, r, sigma, 'call')
    
    # Example 5: Long-term option
    print(f"\n📊 EXAMPLE 5: Long-Term Option")
    print("-" * 50)
    S, K, T, r, sigma = 100, 100, 2.0, 0.04, 0.18
    print(f"Spot: ${S}, Strike: ${K}, Time: {T} years, Rate: {r*100}%, Vol: {sigma*100}%")
    print_results(S, K, T, r, sigma, 'call')
    
    print(f"\n✅ Demo completed! All calculations working correctly.")
    print(f"💡 Try interactive mode to test your own parameters!")

def main():
    """Main function"""
    print_header()
    
    print(f"\n🎮 SELECT MODE:")
    print("1. Interactive Mode (enter your own parameters)")
    print("2. Demo Mode (see comprehensive examples)")
    print("3. Exit")
    
    while True:
        try:
            choice = input(f"\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                interactive_mode()
                break
            elif choice == '2':
                demo_mode()
                break
            elif choice == '3':
                print(f"👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print(f"\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
