from flask import Flask, render_template, request, url_for, session
import numpy as np
import matplotlib
from scipy import stats
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)
app.secret_key = "123"


def generate_data(N, mu, beta0, beta1, sigma2, S):
    # Generate data and initial plots

    # TODO 1: Generate a random dataset X of size N with values between 0 and 1
    X = np.random.rand(N)

    # TODO 2: Generate a random dataset Y using the specified beta0, beta1, mu, and sigma2
    noise = np.random.normal(mu, np.sqrt(sigma2), N)
    Y = beta0 + beta1 * X + noise

    # TODO 3: Fit a linear regression model to X and Y
    model = LinearRegression()
    model.fit(X.reshape(-1, 1), Y)
    slope = model.coef_[0]
    intercept = model.intercept_

    # TODO 4: Generate a scatter plot of (X, Y) with the fitted regression line
    plot1_path = "static/plot1.png"
    plt.figure()
    plt.scatter(X, Y, label="Data Points")
    plt.plot(X, model.predict(X.reshape(-1, 1)), color="red", label=f"y = {slope:.2f}x + {intercept:.2f}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Regression Line: y = {slope:.2f}x + {intercept:.2f}")
    plt.legend()
    plt.savefig(plot1_path)
    plt.close()

    # TODO 5: Run S simulations to generate slopes and intercepts
    slopes = []
    intercepts = []
    print("Sim", S)
    for _ in range(S):
        # TODO 6: Generate simulated datasets using the same beta0 and beta1
        X_sim = np.random.rand(N)
        noise_sim = np.random.normal(mu, np.sqrt(sigma2), N)
        Y_sim = beta0 + beta1 * X_sim + noise_sim

        # TODO 7: Fit linear regression to simulated data and store slope and intercept
        sim_model = LinearRegression()
        sim_model.fit(X_sim.reshape(-1, 1), Y_sim)
        sim_slope = sim_model.coef_[0]
        sim_intercept = sim_model.intercept_

        slopes.append(sim_slope)
        intercepts.append(sim_intercept)

    # TODO 8: Plot histograms of slopes and intercepts
    plot2_path = "static/plot2.png"
    plt.figure(figsize=(10, 5))
    plt.hist(slopes, bins=20, alpha=0.5, color="blue", label="Slopes")
    plt.hist(intercepts, bins=20, alpha=0.5, color="orange", label="Intercepts")
    plt.axvline(slope, color="blue", linestyle="--", linewidth=1, label=f"Slope: {slope:.2f}")
    plt.axvline(intercept, color="orange", linestyle="--", linewidth=1, label=f"Intercept: {intercept:.2f}")
    plt.title("Histogram of Slopes and Intercepts")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.savefig(plot2_path)
    plt.close()
    # Replace with code to generate and save the histogram plot

    # TODO 9: Return data needed for further analysis, including slopes and intercepts
    # Calculate proportions of slopes and intercepts more extreme than observed
    slope_more_extreme = np.mean(np.abs(slopes) > np.abs(slope))
    intercept_extreme = np.mean(np.abs(intercepts) > np.abs(intercept))
    # Return data needed for further analysis
    print("len slopes 1", len(slopes))
    return (
        X,
        Y,
        slope,
        intercept,
        plot1_path,
        plot2_path,
        slope_more_extreme,
        intercept_extreme,
        slopes,
        intercepts,
    )


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input from the form
        N = int(request.form["N"])
        mu = float(request.form["mu"])
        sigma2 = float(request.form["sigma2"])
        beta0 = float(request.form["beta0"])
        beta1 = float(request.form["beta1"])
        S = int(request.form["S"])

        # Generate data and initial plots
        (
            X,
            Y,
            slope,
            intercept,
            plot1,
            plot2,
            slope_extreme,
            intercept_extreme,
            slopes,
            intercepts,
        ) = generate_data(N, mu, beta0, beta1, sigma2, S)

        # # Store data in session
        # session["X"] = X.tolist()
        # session["Y"] = Y.tolist()
        # session["slope"] = slope
        # session["intercept"] = intercept
        # session["slopes"] = slopes
        # session["intercepts"] = intercepts
        # session["slope_extreme"] = slope_extreme
        # session["intercept_extreme"] = intercept_extreme
        # session["N"] = N
        # session["mu"] = mu
        # session["sigma2"] = sigma2
        # session["beta0"] = beta0
        # session["beta1"] = beta1
        # session["S"] = S
        # print(session["N"], "hellooo")
        # Return render_template with variables
        return render_template(
            "index.html",
            plot1=plot1,
            plot2=plot2,
            slope_extreme=slope_extreme,
            intercept_extreme=intercept_extreme,
            N=N,
            mu=mu,
            sigma2=sigma2,
            beta0=beta0,
            beta1=beta1,
            S=S,
        )
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if request.method == "POST":
        # Get user input from the form
        N = int(request.form["N"])
        mu = float(request.form["mu"])
        sigma2 = float(request.form["sigma2"])
        beta0 = float(request.form["beta0"])
        beta1 = float(request.form["beta1"])
        S = int(request.form["S"])

        # Generate data and initial plots
        (
            X,
            Y,
            slope,
            intercept,
            plot1,
            plot2,
            slope_extreme,
            intercept_extreme,
            slopes,
            intercepts,
        ) = generate_data(N, mu, beta0, beta1, sigma2, S)

        # Store data in session
        session["X"] = X.tolist()
        session["Y"] = Y.tolist()
        session["slope"] = slope
        session["intercept"] = intercept
        session["slopes"] = slopes
        session["intercepts"] = intercepts
        session["slope_extreme"] = slope_extreme
        session["intercept_extreme"] = intercept_extreme
        session["N"] = N
        session["mu"] = mu
        session["sigma2"] = sigma2
        session["beta0"] = beta0
        session["beta1"] = beta1
        session["S"] = S
        print(session["N"], "hellooo")
        print("slopes len",len(slopes))
        # Return render_template with variables
        return render_template(
            "index.html",
            plot1=plot1,
            plot2=plot2,
            slope_extreme=slope_extreme,
            intercept_extreme=intercept_extreme,
            N=N,
            mu=mu,
            sigma2=sigma2,
            beta0=beta0,
            beta1=beta1,
            S=S,
        )
    return render_template("index.html")


@app.route("/hypothesis_test", methods=["POST"])
def hypothesis_test():
    # Retrieve data from session
    print(session["S"], "yayy")
    N = int(session.get("N"))
    S = int(session.get("S"))
    slope = float(session.get("slope"))
    intercept = float(session.get("intercept"))
    slopes = session.get("slopes")
    intercepts = session.get("intercepts")
    beta0 = float(session.get("beta0"))
    beta1 = float(session.get("beta1"))
    print("len slopes 2",len(slopes))
    parameter = request.form.get("parameter")
    test_type = request.form.get("test_type")

    # Use the slopes or intercepts from the simulations
    if parameter == "slope":
        simulated_stats = np.array(slopes)
        observed_stat = slope
        hypothesized_value = beta1
    else:
        simulated_stats = np.array(intercepts)
        observed_stat = intercept
        hypothesized_value = beta0

    # TODO 10: Calculate p-value based on test type
    p_value = 0
    if test_type == "Not equal to ( ≠ )":
        p_value = 2 * min(
            np.mean(simulated_stats >= observed_stat),
            np.mean(simulated_stats <= observed_stat)
        )
    elif test_type == "Greater than ( > )":
        p_value = np.mean(simulated_stats <= observed_stat)
    elif test_type == "Less than ( < )":
        p_value = np.mean(simulated_stats >= observed_stat)

    # TODO 11: If p_value is very small (e.g., <= 0.0001), set fun_message to a fun message
    if p_value <= 0.0001:
        fun_message = "Wow, that's a highly significant result!"
    else:
        fun_message = "Looks like a typical day in the world of statistics."

    # TODO 12: Plot histogram of simulated statistics
    plot3_path = "static/plot3.png"
    # Replace with code to generate and save the plot
    plt.figure()
    plt.hist(simulated_stats, bins=30, color='gray', alpha=0.7)
    plt.axvline(observed_stat, color='red', label='Observed Statistic')
    plt.axvline(hypothesized_value, color='blue', linestyle='--', label='Hypothesized Value')
    plt.title(f"Histogram of {parameter} with Observed and Hypothesized Values")
    plt.legend()
    plt.xlabel(parameter)
    plt.ylabel('Frequency')
    plot3_path = "static/plot3.png"
    plt.savefig(plot3_path)
    plt.close()
    print(simulated_stats)

    # Return results to template
    return render_template(
        "index.html",
        plot1="static/plot1.png",
        plot2="static/plot2.png",
        plot3=plot3_path,
        parameter=parameter,
        observed_stat=observed_stat,
        hypothesized_value=hypothesized_value,
        N=N,
        beta0=beta0,
        beta1=beta1,
        S=S,
        # TODO 13: Uncomment the following lines when implemented
        p_value=p_value,
        fun_message=fun_message,
    )

@app.route("/confidence_interval", methods=["POST"])
def confidence_interval():
    # Retrieve data from session
    N = int(session.get("N"))
    mu = float(session.get("mu"))
    sigma2 = float(session.get("sigma2"))
    beta0 = float(session.get("beta0"))
    beta1 = float(session.get("beta1"))
    S = int(session.get("S"))
    X = np.array(session.get("X"))
    Y = np.array(session.get("Y"))
    slope = float(session.get("slope"))
    intercept = float(session.get("intercept"))
    slopes = session.get("slopes")
    intercepts = session.get("intercepts")

    parameter = request.form.get("parameter")
    confidence_level = float(request.form.get("confidence_level"))

    # Use the slopes or intercepts from the simulations
    if parameter == "slope":
        estimates = np.array(slopes)
        observed_stat = slope
        true_param = beta1
    else:
        estimates = np.array(intercepts)
        observed_stat = intercept
        true_param = beta0

    # TODO 14: Calculate mean and standard deviation of the estimates
    mean_estimate = np.mean(estimates)
    std_estimate = np.std(estimates, ddof=1)

    # TODO 15: Calculate confidence interval for the parameter estimate
    # Use the t-distribution and confidence_level
    alpha = 1 - confidence_level/100
    t_value = stats.t.ppf(1 - alpha/2, S-1)
    margin_error = t_value * std_estimate / np.sqrt(S)
    ci_lower = mean_estimate - margin_error
    ci_upper = mean_estimate + margin_error

    # TODO 16: Check if confidence interval includes true parameter
    includes_true = ci_lower <= true_param <= ci_upper


    # TODO 17: Plot the individual estimates as gray points and confidence interval
    # Plot the mean estimate as a colored point which changes if the true parameter is included
    # Plot the confidence interval as a horizontal line
    # Plot the true parameter value
    plot4_path = "static/plot4.png"
    # Write code here to generate and save the plot
    plt.figure(figsize=(10, 6))
    plt.scatter(estimates, [0]*len(estimates), alpha=0.3, color='gray', label='Simulated Estimates')
    plt.scatter(mean_estimate, 0, color='blue' if includes_true else 'red', s=100, label='Mean Estimate')
    plt.hlines(0, ci_lower, ci_upper, color='blue' if includes_true else 'red', linewidth=2, label=f'{confidence_level}% CI')
    plt.axvline(true_param, color='green', linestyle='--', label=f'True {parameter}')
    plt.xlabel(f'{parameter.capitalize()} Estimate')
    plt.title(f'{confidence_level}% Confidence Interval for {parameter.capitalize()} (Mean Estimate)')
    plt.legend()
    plt.savefig(plot4_path)
    plt.close()


    # Return results to template
    return render_template(
        "index.html",
        plot1="static/plot1.png",
        plot2="static/plot2.png",
        plot4=plot4_path,
        parameter=parameter,
        confidence_level=confidence_level,
        mean_estimate=mean_estimate,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        includes_true=includes_true,
        observed_stat=observed_stat,
        N=N,
        mu=mu,
        sigma2=sigma2,
        beta0=beta0,
        beta1=beta1,
        S=S,
    )


if __name__ == "__main__":
    app.run(debug=True)

