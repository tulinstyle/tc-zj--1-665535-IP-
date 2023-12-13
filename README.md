git clone https://github.com/tulinstyle/tc-zj--1-665535-IP-.git
cd tc-zj--1-665535-IP-
chmod +x Hunting-Rabbit-PortScanner.py
扫描单个主机：
python3 Hunting-Rabbit-PortScanner.py 192.168.0.1 -v
扫描网段的所有80端口
python3 Hunting-Rabbit-PortScanner.py 192.168.0.0/24 -v -p 80


## Usage

```
Hunting-Rabbit-PortScanner  author:浪飒

positional arguments:
  network               Network to scan (e.g. "192.168.0.1" or "192.168.0.0/24")

options:
  -h, --help            show this help message and exit
  -p PORTS, --ports PORTS
                        Ports to scan (e.g. "80" or "1-65535", default: 
  -t TIMEOUT, --timeout TIMEOUT
                        TCP connection timeout in seconds (default: 0.5)
  -w WORKERS, --workers WORKERS
                        Maximum number of worker threads for the scan (default: 64)
  -v, --verbose         Verbose output
```

## help

1.如果想提高准确率，可提高超时时间，eg:-t=1。

2.主机存活非ping检测，禁ping也会检测到存活。

3.不检测手机，不在渗透测试范围。
