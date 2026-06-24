---
name: tournament_scheduler
description: Gợi ý và thiết lập thuật toán xếp lịch thi đấu thể thao phức tạp (ràng buộc ngày nghỉ, giờ thi đấu, bảng đấu lệch nhau) bằng thư viện toán học Z3 Solver.
---

# Hướng dẫn xếp lịch thi đấu với Z3 Solver

Khi người dùng yêu cầu xếp lịch cho một giải đấu phức tạp (ví dụ: các bảng đấu có số lượng đội lệch nhau như 5-5-5-4, yêu cầu khắt khe về ngày nghỉ tối thiểu/tối đa, phân bổ khung giờ và cuối tuần), **TUYỆT ĐỐI KHÔNG dùng thuật toán Tham lam (Greedy) hay Quay lui (Backtracking)** vì chúng sẽ bị kẹt (infinite loop). Hãy dùng thư viện **Z3 Theorem Prover**.

## Các nguyên lý thiết kế Z3 cho Lịch thi đấu

1. **Trải phẳng trận đấu (Flatten Matches):** 
   Không nhóm trận đấu theo "Vòng" (Round). Hãy tạo một mảng 1 chiều chứa tất cả các trận đấu của giải.
2. **Khai báo Biến Z3:**
   - `D[i]`: Biến Integer lưu Ngày thi đấu của trận `i`.
   - `T[i]`: Biến Integer lưu Khung giờ thi đấu của trận `i`.
3. **Ràng buộc Cơ sở (Core Constraints):**
   - Giới hạn tổng số trận mỗi ngày và số trận mỗi khung giờ.
4. **Ràng buộc Nghỉ ngơi (Rest Constraints - Rất Quan Trọng):**
   - **Min Rest (Nghỉ tối thiểu):** Các đội không được đá liên tiếp. `Or(D[m1] - D[m2] >= 2, D[m2] - D[m1] >= 2)`
   - **Max Rest (Nghỉ tối đa):** Để tránh việc 1 đội phải đợi 10 ngày mới được đá trận tiếp theo, bạn phải tạo các biến trung gian được sắp xếp (Sorted Variables `S_k`) cho các ngày đá của từng đội, sau đó ép `S[k+1] - S[k] <= max_rest_limit + 1`.
   - **Early Start (Ra quân sớm):** Bắt buộc mọi đội phải có ít nhất 1 trận trong $K$ ngày đầu tiên: `Or([D[m] <= K for m in team_matches])`.
5. **Ràng buộc Công bằng (Fairness Constraints):**
   - **Cuối tuần:** Ép `D[m]` phải rơi vào mảng `weekend_days` ít nhất 1 lần cho mọi đội.
   - **Khung giờ đẹp:** Sử dụng hàm `Sum` để ép tổng số trận rơi vào `T[m] == 1` bằng đúng con số người dùng mong muốn.

## Mã Nguồn Tham Khảo (Reference Code)
Một bản code mẫu siêu tối ưu (chứa tất cả các trick toán học về Max Rest, Early Start, Weekend distribution) đã được lưu tại `examples/z3_reference.py`. 
**LUÔN LUÔN đọc file này trước khi viết thuật toán Z3 mới để tiết kiệm thời gian.**
