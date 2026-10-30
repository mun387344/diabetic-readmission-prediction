import time
import requests
import statistics

API_URL = "http://127.0.0.1:8000/predict"

# Benchmark payload representing a standard patient encounter
TEST_PAYLOAD = {
    "race": "Caucasian",
    "gender": "Female",
    "age": "[60-70)",
    "admission_type_id": 1,
    "discharge_disposition_id": 1,
    "admission_source_id": 7,
    "time_in_hospital": 4,
    "num_lab_procedures": 45,
    "num_procedures": 1,
    "num_medications": 15,
    "number_outpatient": 0,
    "number_emergency": 0,
    "number_inpatient": 1,
    "diag_1": "414",
    "diag_2": "411",
    "diag_3": "250",
    "number_diagnoses": 7,
    "max_glu_serum": "None",
    "A1Cresult": "None",
    "metformin": "No",
    "repaglinide": "No",
    "nateglinide": "No",
    "chlorpropamide": "No",
    "glimepiride": "No",
    "acetohexamide": "No",
    "glipizide": "No",
    "glyburide": "No",
    "tolbutamide": "No",
    "pioglitazone": "No",
    "rosiglitazone": "No",
    "acarbose": "No",
    "miglitol": "No",
    "troglitazone": "No",
    "tolazamide": "No",
    "examide": "No",
    "citoglipton": "No",
    "insulin": "Steady",
    "glyburide-metformin": "No",
    "glipizide-metformin": "No",
    "glimepiride-pioglitazone": "No",
    "metformin-rosiglitazone": "No",
    "metformin-pioglitazone": "No",
    "change": "No",
    "diabetesMed": "Yes"
}

def run_contract_and_latency_audit(num_requests=20):
    latencies = []
    successes = 0

    print(f"Executing {num_requests} automated inference calls against {API_URL}...")

    for i in range(num_requests):
        start_time = time.perf_counter()
        response = requests.post(API_URL, json=TEST_PAYLOAD, timeout=5)
        elapsed = time.perf_counter() - start_time

        if response.status_code == 200:
            successes += 1
            latencies.append(elapsed)
        else:
            print(f"Request {i+1} failed with status {response.status_code}: {response.text}")

    success_rate = (successes / num_requests) * 100
    mean_latency = statistics.mean(latencies)
    p95_latency = sorted(latencies)[int(0.95 * len(latencies))]

    print("\n--- BENCHMARK AUDIT RESULTS ---")
    print(f"Reliability: {success_rate:.1f}% ({successes}/{num_requests} requests successful)")
    print(f"Mean Latency: {mean_latency * 1000:.2f} ms")
    print(f"95th Percentile Latency: {p95_latency * 1000:.2f} ms")
    print(f"Latency Target (<3000 ms): {'PASS' if p95_latency < 3.0 else 'FAIL'}")

if __name__ == "__main__":
    run_contract_and_latency_audit()