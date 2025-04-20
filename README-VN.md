# Rise Testnet Scripts

Kho lưu trữ này chứa một bộ sưu tập các tập lệnh Python được thiết kế để tương tác với **Rise Testnet**, một mạng lưới thử nghiệm blockchain hiệu suất cao. Các tập lệnh này cho phép người dùng thực hiện nhiều hành động khác nhau như gửi giao dịch, triển khai mã thông báo ERC20 và hợp đồng thông minh NFT, quản lý mã thông báo/NFT và tương tác với các ứng dụng phi tập trung (dApp) trên Rise Testnet bằng RPC của nó. Mỗi tập lệnh được xây dựng bằng thư viện `web3.py` và cung cấp hỗ trợ song ngữ (tiếng Anh và tiếng Việt) để tương tác với người dùng.

Faucet: [Rise Testnet Faucet](https://portal.risechain.com/)

## Tổng quan về tính năng

### Tính năng chung

- **Hỗ trợ nhiều tài khoản**: Đọc khóa riêng từ `pvkey.txt` để thực hiện các hành động trên nhiều tài khoản.
- **CLI đầy màu sắc**: Sử dụng `colorama` để tạo đầu ra hấp dẫn về mặt hình ảnh với văn bản và đường viền có màu.
- **Thực thi không đồng bộ**: Được xây dựng bằng `asyncio` để tương tác blockchain hiệu quả.
- **Xử lý lỗi**: Bắt lỗi toàn diện cho các giao dịch blockchain và các vấn đề RPC.
- **Hỗ trợ song ngữ**: Hỗ trợ cả đầu ra tiếng Anh và tiếng Việt dựa trên lựa chọn của người dùng.

### Các tập lệnh được bao gồm

1. **sendtx.py**: Gửi các giao dịch TEA ngẫu nhiên hoặc đến các địa chỉ từ `address.txt` trên Rise Testnet.
2. **deploytoken.py**: Triển khai hợp đồng thông minh mã thông báo ERC20 trên Rise Testnet.
3. **sendtoken.py**: Gửi mã thông báo ERC20 đến các địa chỉ ngẫu nhiên hoặc từ `addressERC20.txt` trên Rise Testnet.
4. **nftcollection.py**: Triển khai và quản lý hợp đồng thông minh NFT (Tạo, Đúc, Đốt) trên Rise Testnet.
5. **gaspump.py**: Thực hiện các hoạt động hoán đổi GasPump trên Rise Testnet.
6. **clober.py**: Thực hiện các hoán đổi Clober (ETH ↔ WETH) trên Rise Testnet.
7. **inari.py**: Quản lý các hoạt động Tài chính Inari (Gửi tiền, Rút tiền) trên Rise Testnet.
8. **wlgtx.py**: Tương tác với WL GTX Dex trên Rise Testnet.
9. **wlnovadubs.py**: Tương tác với WL Novadubs trên Rise Testnet.

## Điều kiện tiên quyết

Trước khi chạy các tập lệnh, hãy đảm bảo bạn đã cài đặt các phần sau:

- Python 3.8+
- `pip` (trình quản lý gói Python)
- **Phụ thuộc**: Cài đặt qua `pip install -r requirements.txt` (đảm bảo `web3.py`, `colorama`, `asyncio`, `eth-account` và `inquirer` được bao gồm).
- **pvkey.txt**: Thêm khóa riêng (mỗi dòng một khóa) để tự động hóa ví.
- Truy cập vào Rise Testnet RPC (ví dụ: https://testnet.riselabs.xyz).
- **address.txt / addressERC20.txt**: Các tệp tùy chọn để chỉ định địa chỉ người nhận.

## Cài đặt

1. **Clone this repository:**
- Mở cmd hoặc Shell, sau đó chạy lệnh:
```sh
git clone https://github.com/thog9/Rise-testnet.git
```
```sh
cd Rise-testnet
```
2. **Install Dependencies:**
- Mở cmd hoặc Shell, sau đó chạy lệnh:
```sh
pip install -r requirements.txt
```
3. **Prepare Input Files:**
- Mở `pvkey.txt`: Thêm khóa riêng của bạn (mỗi dòng một khóa) vào thư mục gốc.
```sh
nano pvkey.txt
```
- Mở `address.txt`(tùy chọn): Thêm địa chỉ người nhận (mỗi dòng một khóa) cho `sendtx.py`, `deploytoken.py`, `sendtoken.py`,`nftcollection.py`, `wlgtx.py`, `wlnovadubs.py`.
```sh
nano address.txt 
```
```sh
nano addressERC20.txt
```
```sh
nano contractERC20.txt
```
```sh
nano contractNFT.txt
```
```sh
nano mail.txt
```
4. **Run:**
- Mở cmd hoặc Shell, sau đó chạy lệnh:
```sh
python main.py
```
- Chọn ngôn ngữ (Tiếng Việt/Tiếng Anh).

## Liên hệ

- **Telegram**: [thog099](https://t.me/thog099)
- **Channel**: [CHANNEL](https://t.me/thogairdrops)
- **Group**: [GROUP CHAT](https://t.me/thogchats)
- **X**: [Thog](https://x.com/thog099) 
