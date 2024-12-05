from locust import events
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os


class CustomReporter:
    def __init__(self):
        self.data = []

    @events.request.add_listener
    def on_request(self, request_type, name, response_time, response_length, exception, **kwargs):
        self.data.append({
            'timestamp': datetime.now(),
            'request_type': request_type,
            'name': name,
            'response_time': response_time,
            'exception': str(exception) if exception else None
        })

    @events.test_stop.add_listener
    def on_test_stop(self, environment, **kwargs):
        if not self.data:
            print("No data collected. Skipping report generation.")
            return

        df = pd.DataFrame(self.data)

        # Ensure the 'reports' directory exists
        os.makedirs('reports', exist_ok=True)

        # Generate P99 response time graph
        self._generate_p99_graph(df)

        # Generate summary report
        self._generate_summary_report(df)

    def _generate_p99_graph(self, df):
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')
        df = df.resample('1T').agg({'response_time': lambda x: x.quantile(0.99)})

        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['response_time'], marker='o')
        plt.title('P99 Response Time Over Time')
        plt.xlabel('Time')
        plt.ylabel('P99 Response Time (ms)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('reports/p99_response_time.png')
        print("P99 response time graph generated: reports/p99_response_time.png")

    def _generate_summary_report(self, df):
        summary = {
            'Total Requests': len(df),
            'Unique Request Types': df['request_type'].nunique(),
            'Unique Endpoints': df['name'].nunique(),
            'Overall Statistics': {
                'Mean Response Time (ms)': df['response_time'].mean(),
                'Median Response Time (ms)': df['response_time'].median(),
                'P95 Response Time (ms)': df['response_time'].quantile(0.95),
                'P99 Response Time (ms)': df['response_time'].quantile(0.99),
                'Max Response Time (ms)': df['response_time'].max(),
                'Min Response Time (ms)': df['response_time'].min(),
            },
            'Exceptions': {
                'Total Exceptions': df['exception'].notna().sum(),
                'Exception Breakdown': df[df['exception'].notna()]['exception'].value_counts().to_dict()
            }
        }

        # Detailed breakdown by request type
        request_type_summary = df.groupby('request_type').agg({
            'response_time': ['count', 'mean', 'median', 'max'],
            'exception': lambda x: x.notna().sum()
        }).reset_index()
        request_type_summary.columns = ['Request Type', 'Total Requests', 'Mean RT (ms)', 'Median RT (ms)',
                                        'Max RT (ms)', 'Exceptions']

        # Detailed breakdown by endpoint
        endpoint_summary = df.groupby('name').agg({
            'response_time': ['count', 'mean', 'median', 'max'],
            'exception': lambda x: x.notna().sum()
        }).reset_index()
        endpoint_summary.columns = ['Endpoint', 'Total Requests', 'Mean RT (ms)', 'Median RT (ms)', 'Max RT (ms)',
                                    'Exceptions']

        with open('reports/performance_summary.txt', 'w') as f:
            f.write("Performance Test Summary Report\n")
            f.write("===============================\n\n")

            # Overall Summary
            f.write("Overall Summary:\n")
            f.write(f"Total Requests: {summary['Total Requests']}\n")
            f.write(f"Unique Request Types: {summary['Unique Request Types']}\n")
            f.write(f"Unique Endpoints: {summary['Unique Endpoints']}\n\n")

            # Overall Statistics
            f.write("Overall Response Time Statistics (ms):\n")
            for stat, value in summary['Overall Statistics'].items():
                f.write(f"{stat}: {value:.2f}\n")
            f.write("\n")

            # Exceptions
            f.write("Exceptions Summary:\n")
            f.write(f"Total Exceptions: {summary['Exceptions']['Total Exceptions']}\n")
            f.write("Exception Breakdown:\n")
            for exc, count in summary['Exceptions']['Exception Breakdown'].items():
                f.write(f"  {exc}: {count}\n")
            f.write("\n")

            # Request Type Summary
            f.write("Request Type Performance Summary:\n")
            f.write(request_type_summary.to_string(index=False))
            f.write("\n\n")

            # Endpoint Summary
            f.write("Endpoint Performance Summary:\n")
            f.write(endpoint_summary.to_string(index=False))

        print("Detailed performance summary generated: reports/performance_summary.txt")
        request_type_summary.to_csv('reports/request_type_summary.csv', index=False)
        endpoint_summary.to_csv('reports/endpoint_summary.csv', index=False)


# Initialize the custom reporter
custom_reporter = CustomReporter()