# EDR Server

EDR Server is a simple Endpoint Detection and Response (EDR) system designed to monitor, detect, and respond to threats on network endpoints. It aims to provide real-time security against malware, ransomware, and other cyber threats, ensuring the integrity and security of networked devices.

## Features

- **Real-time Monitoring:** Continuous observation of endpoint activities to identify suspicious behaviors.
- **Threat Detection:** Advanced algorithms to detect known and unknown threats.
- **Automated Response:** Immediate action on detected threats to mitigate damage.
- **Incident Reporting:** Detailed reports on security incidents for analysis and compliance.
- **Customizable Policies:** Tailor security policies to meet specific organizational needs.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/scrymastic/edr-server.git
```

2. Build the Docker compose file:

```bash
docker-compose build
```

3. Run the Docker compose file:

```bash
docker-compose up
```

4. Access the EDR Server at `http://localhost:8001`. Default credentials are `kali:kali`.

