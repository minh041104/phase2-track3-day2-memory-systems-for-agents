# BENCHMARK — Multi-Memory Agent với LangGraph

**Ngày chạy:** 2026-04-24 11:49

**Model:** gpt-4o-mini

**Token Budget:** 4000


---

## Kết quả Benchmark — 10 Multi-Turn Conversations

| # | Scenario | Group | No-memory result | With-memory result | Pass? |
|---|----------|-------|------------------|---------------------|-------|
| 1 | Profile Recall — Nhớ tên user sau nhiều turns | profile_recall | Có, bạn tên là Linh! Rất vui được tiếp tục trò chu... | Có chứ, bạn tên là Linh! Rất vui được nhớ tên bạn.... | ✅ Pass |
| 2 | Profile Recall — Nhớ nhiều facts cùng lúc | profile_recall | Chào Minh! Tôi biết bạn là 22 tuổi, sống ở Hà Nội ... | Tôi biết bạn tên là Minh, 22 tuổi và sống ở Hà Nội... | ✅ Pass |
| 3 | Conflict Update — Sửa dị ứng | conflict_update | Bạn dị ứng với đậu nành. Nếu bạn cần bất kỳ thông ... | Bạn dị ứng với đậu nành. Hãy nhớ tránh các sản phẩ... | ✅ Pass |
| 4 | Conflict Update — Đổi nghề nghiệp | conflict_update | Nghề nghiệp hiện tại của bạn là data scientist. Nế... | Nghề nghiệp hiện tại của bạn là data scientist. Bạ... | ✅ Pass |
| 5 | Episodic Recall — Nhớ bài học debug | episodic_recall | Bài học hôm trước của bạn về Docker liên quan đến ... | Bài học hôm trước của bạn về Docker liên quan đến ... | ✅ Pass |
| 6 | Episodic Recall — Nhớ task đã hoàn thành | episodic_recall | Project gần đây nhất mà bạn đã hoàn thành là việc ... | Dự án gần đây nhất bạn đã hoàn thành là việc deplo... | ✅ Pass |
| 7 | Semantic Retrieval — Docker networking FAQ | semantic_retrieval | Để các container Docker giao tiếp với nhau, bạn có... | Trong Docker Compose, các container giao tiếp với ... | ❌ Fail |
| 8 | Semantic Retrieval — API Security | semantic_retrieval | Để bảo mật API của bạn, bạn có thể thực hiện các b... | Để bảo mật API của bạn, bạn có thể thực hiện các b... | ✅ Pass |
| 9 | Token Budget — Conversation dài vẫn hoạt động | trim_token_budget | Có chứ, Hùng! Bạn đang ở Đà Nẵng. Có điều gì khác ... | Có, Hùng! Bạn đang sống ở Đà Nẵng. Bạn có điều gì ... | ✅ Pass |
| 10 | Combined — Profile + Semantic + Episodic | trim_token_budget | Tối ưu hóa database là một bước quan trọng để cải ... | Tất nhiên rồi, Anh! Dưới đây là một số gợi ý để tố... | ✅ Pass |

**Summary:** No-memory 10/10 | With-memory 9/10

---

## Chi tiết từng Conversation

### Scenario 1: Profile Recall — Nhớ tên user sau nhiều turns

**Group:** profile_recall

**Mô tả:** Agent cần nhớ tên user 'Linh' sau 6 turns hội thoại

**Expected keyword:** `Linh`


#### 🚫 No-Memory

**User (turn 1):** Xin chào, tôi tên là Linh.

**Agent:** Xin chào Linh! Rất vui được gặp bạn. Bạn có điều gì muốn hỏi hoặc chia sẻ không?

**User (turn 2):** Tôi là sinh viên năm 3 ngành CNTT.

**Agent:** Rất vui được biết bạn là sinh viên năm 3 ngành Công nghệ Thông tin, Linh! Bạn có đang học về lĩnh vực nào cụ thể trong CNTT không? Hoặc có điều gì bạn muốn hỏi hoặc thảo luận về ngành học của mình?

**User (turn 3):** Tôi thích lập trình Python.

**Agent:** Thật tuyệt vời khi biết bạn thích lập trình Python, Linh! Python là một ngôn ngữ rất linh hoạt và dễ học, đặc biệt là đối với sinh viên CNTT. Bạn có đang làm dự án nào liên quan đến Python không, hoặc...

**User (turn 4):** Hôm nay trời đẹp quá nhỉ?

**Agent:** Thật tuyệt khi nghe bạn cảm nhận được thời tiết đẹp, Linh! Một ngày đẹp trời thường rất phù hợp để thư giãn hoặc ra ngoài làm những điều mình thích. Bạn có kế hoạch gì cho hôm nay không?

**User (turn 5):** À mà sở thích của tôi là chơi guitar.

**Agent:** Rất vui khi biết rằng sở thích của bạn là chơi guitar, Linh! Chơi nhạc cụ không chỉ giúp giải tỏa căng thẳng mà còn là một cách thú vị để thể hiện bản thân. Bạn đã chơi guitar được bao lâu rồi? Bạn th...

**User (turn 6):** Bạn có nhớ tên tôi không?

**Agent:** Có, bạn tên là Linh! Rất vui được tiếp tục trò chuyện với bạn. Bạn có điều gì muốn hỏi hoặc chia sẻ không?


**Result:** ✅ PASS


#### 🧠 With-Memory

**User (turn 1):** Xin chào, tôi tên là Linh.

**Agent:** Xin chào Linh! Rất vui được gặp bạn. Bạn có điều gì muốn chia sẻ hoặc hỏi hôm nay không?

**User (turn 2):** Tôi là sinh viên năm 3 ngành CNTT.

**Agent:** Rất vui được biết bạn là sinh viên năm 3 ngành CNTT, Linh! Bạn đang học tập ở trường nào? Có điều gì thú vị hoặc thách thức trong quá trình học mà bạn muốn chia sẻ không?

**User (turn 3):** Tôi thích lập trình Python.

**Agent:** Thật tuyệt vời khi biết rằng bạn thích lập trình Python, Linh! Python là một ngôn ngữ rất mạnh mẽ và linh hoạt, đặc biệt là trong lĩnh vực CNTT. Bạn đã làm gì với Python chưa? Có dự án nào thú vị mà b...

**User (turn 4):** Hôm nay trời đẹp quá nhỉ?

**Agent:** Có vẻ như hôm nay là một ngày tuyệt vời, Linh! Thời tiết đẹp có thể mang lại cảm giác thoải mái và làm cho ngày học tập hoặc làm việc trở nên dễ chịu hơn. Bạn có kế hoạch gì cho ngày hôm nay không?

**User (turn 5):** À mà sở thích của tôi là chơi guitar.

**Agent:** Cảm ơn Linh đã chia sẻ! Vậy là bạn có sở thích chơi guitar bên cạnh lập trình Python. Thật tuyệt vời! Bạn đã chơi guitar được bao lâu rồi? Có bài hát nào bạn thích chơi không?

**User (turn 6):** Bạn có nhớ tên tôi không?

**Agent:** Có chứ, bạn tên là Linh! Rất vui được nhớ tên bạn. Bạn có điều gì muốn chia sẻ hoặc hỏi hôm nay không?


**Result:** ✅ PASS

**Profile state:** `{"name": "Linh", "job": "sinh viên", "major": "CNTT", "year": 3, "hobby": "chơi guitar"}`

---

### Scenario 2: Profile Recall — Nhớ nhiều facts cùng lúc

**Group:** profile_recall

**Mô tả:** Agent cần nhớ tên, tuổi, nơi ở, công việc

**Expected keyword:** `Minh`


#### 🚫 No-Memory

**User (turn 1):** Tôi tên Minh, 22 tuổi, sống ở Hà Nội.

**Agent:** Chào Minh! Rất vui được biết bạn. Bạn có sở thích gì hoặc đang làm gì trong cuộc sống?

**User (turn 2):** Tôi làm việc tại FPT Software.

**Agent:** Rất tuyệt Minh! Làm việc tại FPT Software chắc chắn mang lại cho bạn nhiều cơ hội thú vị. Bạn đang làm ở vị trí nào tại công ty?

**User (turn 3):** Cho tôi biết những gì bạn biết về tôi?

**Agent:** Chào Minh! Tôi biết bạn là 22 tuổi, sống ở Hà Nội và đang làm việc tại FPT Software. Nếu bạn có thêm thông tin nào muốn chia sẻ hoặc có câu hỏi gì, đừng ngần ngại nhé!


**Result:** ✅ PASS


#### 🧠 With-Memory

**User (turn 1):** Tôi tên Minh, 22 tuổi, sống ở Hà Nội.

**Agent:** Chào Minh! Rất vui được biết bạn. Bạn có sở thích hay lĩnh vực nào mà bạn muốn chia sẻ không?

**User (turn 2):** Tôi làm việc tại FPT Software.

**Agent:** Rất tuyệt, Minh! FPT Software là một trong những công ty công nghệ hàng đầu tại Việt Nam. Bạn đang làm việc ở vị trí nào tại đó?

**User (turn 3):** Cho tôi biết những gì bạn biết về tôi?

**Agent:** Tôi biết bạn tên là Minh, 22 tuổi và sống ở Hà Nội. Bạn làm việc tại FPT Software. Nếu bạn có thêm thông tin nào khác muốn chia sẻ hoặc có câu hỏi nào, hãy cho tôi biết nhé!


**Result:** ✅ PASS

**Profile state:** `{"name": "Minh", "age": 22, "location": "Hà Nội", "job": "FPT Software"}`

---

### Scenario 3: Conflict Update — Sửa dị ứng

**Group:** conflict_update

**Mô tả:** Agent cần update dị ứng từ 'sữa bò' → 'đậu nành'

**Expected keyword:** `đậu nành`


#### 🚫 No-Memory

**User (turn 1):** Tôi dị ứng sữa bò.

**Agent:** Cảm ơn bạn đã chia sẻ thông tin! Bạn đã cho biết rằng bạn dị ứng với sữa bò. Khi nấu ăn hoặc chọn thực phẩm, hãy nhớ kiểm tra kỹ thành phần để tránh các sản phẩm có chứa sữa bò. Nếu bạn cần lời khuyên...

**User (turn 2):** À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò.

**Agent:** Cảm ơn bạn đã cập nhật thông tin! Vậy là bạn dị ứng với đậu nành. Khi lựa chọn thực phẩm hoặc nấu ăn, hãy nhớ kiểm tra kỹ thành phần để tránh các sản phẩm có chứa đậu nành. Nếu bạn cần lời khuyên về c...

**User (turn 3):** Tôi dị ứng gì vậy?

**Agent:** Bạn dị ứng với đậu nành. Nếu bạn cần bất kỳ thông tin nào về chế độ ăn uống hoặc công thức nấu ăn không có đậu nành, cứ cho tôi biết nhé!


**Result:** ✅ PASS


#### 🧠 With-Memory

**User (turn 1):** Tôi dị ứng sữa bò.

**Agent:** Cảm ơn bạn đã chia sẻ thông tin này! Bạn nên tránh các sản phẩm chứa sữa bò và kiểm tra kỹ thành phần trong thực phẩm để đảm bảo an toàn cho sức khỏe của mình. Nếu bạn cần thêm thông tin về các thực p...

**User (turn 2):** À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò.

**Agent:** Cảm ơn bạn đã cập nhật thông tin! Vậy bạn dị ứng với đậu nành. Hãy chắc chắn tránh các sản phẩm chứa đậu nành và kiểm tra kỹ thành phần thực phẩm. Nếu bạn cần thêm thông tin về các thực phẩm thay thế ...

**User (turn 3):** Tôi dị ứng gì vậy?

**Agent:** Bạn dị ứng với đậu nành. Hãy nhớ tránh các sản phẩm chứa đậu nành và kiểm tra kỹ thành phần thực phẩm để đảm bảo an toàn cho sức khỏe của bạn. Nếu bạn cần thêm thông tin hoặc gợi ý về thực phẩm thay t...


**Result:** ✅ PASS

**Profile state:** `{"allergy": "đậu nành"}`

---

### Scenario 4: Conflict Update — Đổi nghề nghiệp

**Group:** conflict_update

**Mô tả:** Agent cần update nghề từ 'kỹ sư phần mềm' → 'data scientist'

**Expected keyword:** `data scientist`


#### 🚫 No-Memory

**User (turn 1):** Tôi là kỹ sư phần mềm.

**Agent:** Chào bạn! Rất vui được biết bạn là kỹ sư phần mềm. Bạn đang làm việc với công nghệ nào, hoặc có dự án nào thú vị mà bạn đang tham gia không?

**User (turn 2):** Thực ra, tôi vừa chuyển sang làm data scientist.

**Agent:** Chúc mừng bạn đã chuyển sang làm data scientist! Đó là một lĩnh vực thú vị và đầy thử thách. Bạn có đang làm việc với công nghệ hay công cụ nào cụ thể trong lĩnh vực này không?

**User (turn 3):** Nghề nghiệp hiện tại của tôi là gì?

**Agent:** Nghề nghiệp hiện tại của bạn là data scientist. Nếu bạn có bất kỳ câu hỏi nào liên quan đến lĩnh vực này hoặc muốn chia sẻ thêm về công việc của mình, hãy cho tôi biết nhé!


**Result:** ✅ PASS


#### 🧠 With-Memory

**User (turn 1):** Tôi là kỹ sư phần mềm.

**Agent:** Rất vui được biết bạn là kỹ sư phần mềm! Bạn đang làm việc trong lĩnh vực nào của công nghệ thông tin, và có dự án nào thú vị mà bạn đang tham gia không?

**User (turn 2):** Thực ra, tôi vừa chuyển sang làm data scientist.

**Agent:** Chúc mừng bạn đã chuyển sang làm data scientist! Đây là một lĩnh vực rất thú vị và có nhiều tiềm năng. Bạn đang làm việc trong lĩnh vực nào của khoa học dữ liệu, và có dự án nào đặc biệt mà bạn đang t...

**User (turn 3):** Nghề nghiệp hiện tại của tôi là gì?

**Agent:** Nghề nghiệp hiện tại của bạn là data scientist. Bạn đang làm việc trong lĩnh vực này và đã có sự chuyển đổi từ kỹ sư phần mềm. Có dự án nào đặc biệt mà bạn đang tham gia không?


**Result:** ✅ PASS

**Profile state:** `{"job": "data scientist"}`

---

### Scenario 5: Episodic Recall — Nhớ bài học debug

**Group:** episodic_recall

**Mô tả:** Agent cần recall bài học 'dùng service name thay vì localhost'

**Expected keyword:** `service name`


#### 🚫 No-Memory

**User (turn 1):** Hôm qua tôi debug lỗi Docker cả ngày. Cuối cùng phát hiện ra là phải dùng service name thay vì localhost.

**Agent:** Rất vui khi bạn đã tìm ra nguyên nhân của lỗi Docker! Đúng như bạn đã phát hiện, trong Docker Compose, các container giao tiếp với nhau qua service name chứ không phải localhost. Điều này có thể gây n...

**User (turn 2):** Tôi được bài học quan trọng về networking trong Docker.

**Agent:** Rất tuyệt! Việc hiểu rõ về networking trong Docker là rất quan trọng để có thể cấu hình và quản lý các container một cách hiệu quả. Bạn có thể chia sẻ thêm về bài học cụ thể nào mà bạn đã rút ra không...

**User (turn 3):** Nhắc lại giúp tôi bài học về Docker hôm trước?

**Agent:** Bài học hôm trước của bạn về Docker liên quan đến việc sử dụng service name thay vì localhost để giao tiếp giữa các container. Bạn đã phát hiện ra rằng trong Docker Compose, các container giao tiếp vớ...


**Result:** ✅ PASS


#### 🧠 With-Memory

**User (turn 1):** Hôm qua tôi debug lỗi Docker cả ngày. Cuối cùng phát hiện ra là phải dùng service name thay vì localhost.

**Agent:** Rất tốt khi bạn đã phát hiện ra vấn đề đó! Trong Docker Compose, đúng như bạn đã nói, các container giao tiếp với nhau qua service name chứ không phải localhost. Việc sử dụng service name giúp đảm bảo...

**User (turn 2):** Tôi được bài học quan trọng về networking trong Docker.

**Agent:** Rất tuyệt vời! Việc bạn học được về networking trong Docker, đặc biệt là cách sử dụng service name để giao tiếp giữa các container, là rất quan trọng. Điều này giúp bạn tránh được những lỗi phổ biến v...

**User (turn 3):** Nhắc lại giúp tôi bài học về Docker hôm trước?

**Agent:** Bài học hôm trước của bạn về Docker liên quan đến việc sử dụng service name thay vì localhost để giao tiếp giữa các container. Bạn đã phát hiện ra rằng trong Docker Compose, các container cần kết nối ...


**Result:** ✅ PASS

---

### Scenario 6: Episodic Recall — Nhớ task đã hoàn thành

**Group:** episodic_recall

**Mô tả:** Agent cần recall task 'deploy API lên Railway'

**Expected keyword:** `Railway`


#### 🚫 No-Memory

**User (turn 1):** Tôi vừa hoàn thành project deploy API lên Railway thành công.

**Agent:** Chúc mừng bạn đã hoàn thành project deploy API lên Railway! Thật tuyệt vời khi thấy nỗ lực của bạn đã được đền đáp. Bạn có gặp phải khó khăn gì trong quá trình triển khai không, hay có điều gì thú vị ...

**User (turn 2):** Tôi đã học được cách setup health check endpoint.

**Agent:** Thật tuyệt vời! Việc thiết lập health check endpoint là một bước quan trọng trong quá trình triển khai ứng dụng, giúp bạn theo dõi tình trạng của API và phát hiện sớm các vấn đề. Bạn có gặp phải khó k...

**User (turn 3):** Nhắc tôi về project gần đây nhất tôi đã làm?

**Agent:** Project gần đây nhất mà bạn đã hoàn thành là việc triển khai một API trên nền tảng Railway. Bạn đã thành công trong việc này và cũng đã học được cách thiết lập health check endpoint. Bạn có muốn chia ...


**Result:** ✅ PASS


#### 🧠 With-Memory

**User (turn 1):** Tôi vừa hoàn thành project deploy API lên Railway thành công.

**Agent:** Chúc mừng bạn đã hoàn thành dự án và deploy API lên Railway thành công! Đó là một bước tiến lớn. Bạn có gặp phải khó khăn nào trong quá trình này không? Hay bạn có kế hoạch gì tiếp theo cho dự án của ...

**User (turn 2):** Tôi đã học được cách setup health check endpoint.

**Agent:** Thật tuyệt! Việc thiết lập health check endpoint là rất quan trọng để đảm bảo rằng ứng dụng của bạn hoạt động ổn định và có thể được giám sát hiệu quả. Bạn có gặp khó khăn gì trong quá trình thiết lập...

**User (turn 3):** Nhắc tôi về project gần đây nhất tôi đã làm?

**Agent:** Dự án gần đây nhất bạn đã hoàn thành là việc deploy API lên Railway. Trong quá trình đó, bạn cũng đã học được cách thiết lập health check endpoint. Nếu bạn cần thêm thông tin hay hỗ trợ gì về dự án nà...


**Result:** ✅ PASS

**Profile state:** `{"project": "deploy API lên Railway", "learning": "setup health check endpoint"}`

---

### Scenario 7: Semantic Retrieval — Docker networking FAQ

**Group:** semantic_retrieval

**Mô tả:** Agent cần retrieve knowledge về Docker networking từ semantic memory

**Expected keyword:** `service name`


#### 🚫 No-Memory

**User (turn 1):** Làm sao để các container Docker nói chuyện với nhau?

**Agent:** Để các container Docker giao tiếp với nhau, bạn có thể sử dụng Docker Compose. Trong Docker Compose, các container giao tiếp với nhau qua service name thay vì sử dụng địa chỉ localhost. 

Ví dụ, nếu b...

**User (turn 2):** Cho tôi ví dụ cụ thể hơn về cách kết nối?

**Agent:** Chắc chắn rồi! Dưới đây là một ví dụ cụ thể về cách kết nối các container Docker với nhau sử dụng Docker Compose.

Giả sử bạn có một ứng dụng web đơn giản với một container cho server (ví dụ: Node.js)...


**Result:** ✅ PASS


#### 🧠 With-Memory

**User (turn 1):** Làm sao để các container Docker nói chuyện với nhau?

**Agent:** Trong Docker Compose, các container giao tiếp với nhau qua tên service chứ không phải thông qua `localhost`. Ví dụ, nếu bạn có một service tên là `db`, các container khác sẽ kết nối với nó bằng cách s...

**User (turn 2):** Cho tôi ví dụ cụ thể hơn về cách kết nối?

**Agent:** Để minh họa cụ thể hơn về cách kết nối giữa các container Docker, hãy xem xét một ví dụ đơn giản với hai service: một service là `web` (ứng dụng web) và một service là `db` (cơ sở dữ liệu). Dưới đây l...


**Result:** ❌ FAIL

---

### Scenario 8: Semantic Retrieval — API Security

**Group:** semantic_retrieval

**Mô tả:** Agent cần retrieve knowledge về API security từ semantic memory

**Expected keyword:** `JWT`


#### 🚫 No-Memory

**User (turn 1):** Tôi cần bảo mật API của mình, nên làm gì?

**Agent:** Để bảo mật API của bạn, bạn có thể thực hiện các biện pháp sau:

1. **Sử dụng HTTPS**: Đảm bảo tất cả các kết nối đến API đều sử dụng HTTPS để mã hóa dữ liệu truyền tải.

2. **Implement JWT Authentica...

**User (turn 2):** JWT là gì và dùng như thế nào?

**Agent:** JWT (JSON Web Token) là một tiêu chuẩn mở (RFC 7519) cho phép truyền tải thông tin an toàn giữa các bên dưới dạng một đối tượng JSON. Thông tin này có thể được xác minh và tin cậy nhờ vào chữ ký số. J...


**Result:** ✅ PASS


#### 🧠 With-Memory

**User (turn 1):** Tôi cần bảo mật API của mình, nên làm gì?

**Agent:** Để bảo mật API của bạn, bạn có thể thực hiện các biện pháp sau:

1. **Sử dụng HTTPS**: Đảm bảo rằng tất cả các giao tiếp giữa client và server đều được mã hóa bằng HTTPS để bảo vệ dữ liệu khỏi bị nghe...

**User (turn 2):** JWT là gì và dùng như thế nào?

**Agent:** JWT (JSON Web Token) là một tiêu chuẩn mở (RFC 7519) cho phép truyền thông tin giữa các bên một cách an toàn dưới dạng một đối tượng JSON. Thông tin trong JWT có thể được xác thực và tin cậy vì nó đượ...


**Result:** ✅ PASS

---

### Scenario 9: Token Budget — Conversation dài vẫn hoạt động

**Group:** trim_token_budget

**Mô tả:** Agent vẫn nhớ thông tin quan trọng sau conversation dài (9 turns)

**Expected keyword:** `Hùng`


#### 🚫 No-Memory

**User (turn 1):** Tôi tên là Hùng.

**Agent:** Chào Hùng! Rất vui được gặp bạn. Bạn có điều gì muốn hỏi hay chia sẻ không?

**User (turn 2):** Tôi thích ăn phở.

**Agent:** Phở là một món ăn rất ngon và phổ biến ở Việt Nam! Bạn thích phở bò hay phở gà hơn? Hay có một loại phở đặc biệt nào mà bạn yêu thích không?

**User (turn 3):** Tôi ở Đà Nẵng.

**Agent:** Thật tuyệt vời! Đà Nẵng là một thành phố đẹp với nhiều bãi biển và món ăn ngon. Bạn có thường thưởng thức phở ở Đà Nẵng không? Hay có món ăn nào khác mà bạn thích ở đó không?

**User (turn 4):** Tôi học Machine Learning.

**Agent:** Thật tuyệt vời, Hùng! Machine Learning là một lĩnh vực rất thú vị và có nhiều ứng dụng thực tiễn. Bạn đang học về các chủ đề cụ thể nào trong Machine Learning? Hay có dự án nào mà bạn đang làm không?

**User (turn 5):** Tôi dùng PyTorch.

**Agent:** Tuyệt quá, Hùng! PyTorch là một thư viện rất mạnh mẽ cho Machine Learning và Deep Learning. Bạn đang làm việc với loại mô hình nào trong PyTorch? Có dự án hoặc bài tập cụ thể nào mà bạn đang thực hiện...

**User (turn 6):** Tôi làm freelance.

**Agent:** Thật tuyệt, Hùng! Bạn làm freelance trong lĩnh vực nào? Có phải là về Machine Learning không?

**User (turn 7):** Tôi thích đọc sách.

**Agent:** Thật tuyệt vời, Hùng! Đọc sách là một cách tuyệt vời để mở rộng kiến thức và thư giãn. Bạn thích đọc thể loại sách nào? Có cuốn sách nào gần đây mà bạn cảm thấy ấn tượng không?

**User (turn 8):** Tôi hay chạy bộ buổi sáng.

**Agent:** Tuyệt vời, Hùng! Chạy bộ buổi sáng là một cách tuyệt vời để khởi động ngày mới và giữ gìn sức khỏe. Bạn thường chạy ở đâu tại Đà Nẵng? Có phải là ở bãi biển hay công viên nào không?

**User (turn 9):** Bạn có nhớ tên tôi và tôi ở đâu không?

**Agent:** Có chứ, Hùng! Bạn đang ở Đà Nẵng. Có điều gì khác mà bạn muốn chia sẻ không?


**Result:** ✅ PASS


#### 🧠 With-Memory

**User (turn 1):** Tôi tên là Hùng.

**Agent:** Chào Hùng! Rất vui được biết bạn. Bạn có điều gì muốn chia sẻ hoặc hỏi không?

**User (turn 2):** Tôi thích ăn phở.

**Agent:** Phở là một món ăn rất ngon và nổi tiếng ở Việt Nam! Bạn thích phở bò hay phở gà hơn? Nếu có quán phở nào bạn thường ghé, hãy chia sẻ với mình nhé!

**User (turn 3):** Tôi ở Đà Nẵng.

**Agent:** Rất tuyệt! Đà Nẵng là một thành phố xinh đẹp với nhiều danh lam thắng cảnh. Bạn có thích những món ăn đặc sản nào ở Đà Nẵng không? Ngoài phở, có món nào khác mà bạn yêu thích không?

**User (turn 4):** Tôi học Machine Learning.

**Agent:** Wow, thật tuyệt vời! Machine Learning là một lĩnh vực rất thú vị và đang phát triển mạnh mẽ. Bạn đang học về những chủ đề nào trong Machine Learning? Có dự án nào bạn đang tham gia không?

**User (turn 5):** Tôi dùng PyTorch.

**Agent:** Thật tuyệt vời! PyTorch là một thư viện rất phổ biến trong lĩnh vực Machine Learning, đặc biệt là trong deep learning. Bạn đang làm việc với dự án nào trong PyTorch? Có chủ đề cụ thể nào bạn đang nghi...

**User (turn 6):** Tôi làm freelance.

**Agent:** Rất tốt, Hùng! Thế là bạn đang làm freelance trong lĩnh vực Machine Learning. Bạn có thể chia sẻ thêm về loại dự án nào mà bạn thường làm, hay bạn đang tìm kiếm khách hàng mới không?

**User (turn 7):** Tôi thích đọc sách.

**Agent:** Thật tuyệt vời, Hùng! Đọc sách là một cách tuyệt vời để mở rộng kiến thức và thư giãn. Bạn thích thể loại sách nào? Có cuốn sách nào đặc biệt mà bạn muốn giới thiệu không?

**User (turn 8):** Tôi hay chạy bộ buổi sáng.

**Agent:** Thật tuyệt vời, Hùng! Chạy bộ buổi sáng là một cách tuyệt vời để khởi động ngày mới và duy trì sức khỏe. Bạn thường chạy ở đâu tại Đà Nẵng? Có lộ trình yêu thích nào mà bạn muốn chia sẻ không?

**User (turn 9):** Bạn có nhớ tên tôi và tôi ở đâu không?

**Agent:** Có, Hùng! Bạn đang sống ở Đà Nẵng. Bạn có điều gì muốn chia sẻ thêm không?


**Result:** ✅ PASS

**Profile state:** `{"name": "Hùng", "favorite_food": "phở", "location": "Đà Nẵng", "job": "freelance", "framework": "PyTorch", "hobby": "running"}`

---

### Scenario 10: Combined — Profile + Semantic + Episodic

**Group:** trim_token_budget

**Mô tả:** Agent kết hợp profile (tên), episodic (JWT task), và semantic (DB optimization)

**Expected keyword:** `index`


#### 🚫 No-Memory

**User (turn 1):** Tôi tên Anh, là dev Python.

**Agent:** Chào Anh! Rất vui được biết bạn là một developer Python. Bạn đang làm việc trên dự án nào hiện tại? Nếu cần hỗ trợ hoặc có câu hỏi về Python, đừng ngần ngại hỏi nhé!

**User (turn 2):** Hôm qua tôi lập trình xong feature authentication dùng JWT.

**Agent:** Thật tuyệt vời! Việc sử dụng JWT cho tính năng xác thực là một cách rất hiệu quả. Bạn có gặp khó khăn gì trong quá trình triển khai không? Hoặc nếu cần chia sẻ thêm về cách bạn đã thực hiện, mình rất ...

**User (turn 3):** Giờ tôi muốn tối ưu database, bạn có gợi ý gì dựa trên kinh nghiệm và kiến thức không?

**Agent:** Tối ưu hóa database là một bước quan trọng để cải thiện hiệu suất ứng dụng của bạn. Dưới đây là một số gợi ý mà bạn có thể áp dụng:

1. **Sử dụng Index**: Tạo index cho các cột thường xuyên được truy ...


**Result:** ✅ PASS


#### 🧠 With-Memory

**User (turn 1):** Tôi tên Anh, là dev Python.

**Agent:** Chào Anh! Rất vui được biết bạn là một developer Python. Nếu bạn có bất kỳ câu hỏi nào về Python hoặc cần hỗ trợ gì trong quá trình phát triển, hãy cho tôi biết nhé!

**User (turn 2):** Hôm qua tôi lập trình xong feature authentication dùng JWT.

**Agent:** Chúc mừng Anh đã hoàn thành feature authentication sử dụng JWT! Đây là một bước quan trọng trong việc bảo mật ứng dụng. Nếu Anh cần bất kỳ hỗ trợ nào về việc triển khai hoặc kiểm tra tính năng này, hã...

**User (turn 3):** Giờ tôi muốn tối ưu database, bạn có gợi ý gì dựa trên kinh nghiệm và kiến thức không?

**Agent:** Tất nhiên rồi, Anh! Dưới đây là một số gợi ý để tối ưu database mà bạn có thể tham khảo:

1. **Sử dụng Index**: Tạo index cho các cột mà thường xuyên được truy vấn. Điều này giúp tăng tốc độ truy vấn ...


**Result:** ✅ PASS

**Profile state:** `{"name": "Anh", "job": "Python developer", "feature": "authentication", "technology": "JWT"}`

---

## Reflection — Privacy & Limitations


### 1. Memory nào giúp agent nhất?

**Long-term Profile Memory** giúp agent nhất vì cho phép cá nhân hóa mọi response.
Khi biết tên, nghề nghiệp, sở thích, dị ứng của user, agent có thể trả lời chính xác
và thân thiện hơn. **Semantic Memory** đứng thứ hai vì cung cấp knowledge factual
mà agent không thể tự biết.

### 2. Memory nào rủi ro nhất nếu retrieve sai?

**Long-term Profile Memory** rủi ro nhất:
- Nếu retrieve sai thông tin dị ứng → có thể gây nguy hiểm sức khỏe (khuyên ăn thứ user dị ứng)
- Thông tin cá nhân (tên, tuổi, nghề) nếu sai sẽ khiến user mất niềm tin
- PII (Personally Identifiable Information) stored dạng plaintext → risk nếu bị leak

**Episodic Memory** cũng rủi ro nếu ghi nhớ sai bài học → agent tái sử dụng kiến thức sai.

### 3. Nếu user yêu cầu xóa memory, xóa ở backend nào?

Cần xóa ở **tất cả backends**:
- **Short-term:** `clear()` — dễ nhất, chỉ là buffer trong RAM
- **Long-term Profile:** `delete_fact(key)` hoặc `clear()` — xóa file JSON
- **Episodic:** `delete_episode(id)` hoặc `clear()` — xóa file JSON
- **Semantic:** `delete_document(id)` hoặc `clear()` — xóa từ ChromaDB

Hiện tại system **chưa có cơ chế consent rõ ràng** (GDPR Right to be Forgotten).
Cần implement:
- Thông báo user trước khi lưu PII
- Cho phép user opt-out từng loại memory
- TTL (Time-To-Live) cho Profile facts — auto-expire sau N ngày
- Audit log cho mọi operation trên PII

### 4. Điều gì sẽ làm system fail khi scale?

**Limitations kỹ thuật:**

1. **JSON file-based storage** (Profile + Episodic): Không scale khi có nhiều users.
   Cần migrate sang Redis/PostgreSQL cho production.

2. **ChromaDB single-node**: Giới hạn khoảng 1M documents.
   Cần distributed vector DB (Pinecone, Weaviate) cho scale.

3. **LLM-based fact extraction**: Mỗi turn gọi thêm 1 lần LLM để extract facts
   → tăng latency và cost gấp đôi. Cần caching hoặc rule-based extraction cho facts đơn giản.

4. **Token budget**: Khi 4 loại memory đều lớn, trim có thể cắt mất thông tin quan trọng.
   Cần smarter prioritization (dùng relevance score thay vì order-based trim).

5. **Conflict detection**: Hoàn toàn phụ thuộc vào LLM → false positives/negatives.
   Cần hybrid approach: rule-based cho exact matches + LLM cho semantic conflicts.

6. **No encryption**: PII lưu plaintext trong JSON/ChromaDB.
   Production cần encryption at rest + in transit.

7. **Single-thread**: Không hỗ trợ concurrent users.
   Cần session management + per-user memory isolation.
