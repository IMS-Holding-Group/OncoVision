# OncoVision

تطبيق ويب Flask لتحليل صور الماموجرام بنموذج YOLOv8، مع حسابات مستخدمين ونتائج في SQLite. الوصف في README السابق يسميه نظام تحليل ماموجرام بالذكاء الاصطناعي لفئة `tumor`.

## 1. ما هو المشروع؟

واجهة ويب ترفع صورة، تشغّل استنتاج YOLO، وتحفظ إن وُجد كشف وعدد الكشوفات والثقة وزمن المعالجة ومسار صورة مخرجة. الملفات: `app.py`, `infer.py`, `train.py`, `evaluate.py`, `templates`, `static`.

## 2. لماذا يوجد هذا المشروع؟

تعليق `app.py` يقول: واجهة ويب لتحليل الماموجرام باستخدام YOLOv8. README السابق يصف المساعدة في النظر إلى صور الماموجرام واكتشاف مناطق مصنفة `tumor`. اعتماد طبي رسمي غير موثق في الكود.

## 3. من يستخدمه؟

جدول `users` فيه `username` و `role` (القيمة الافتراضية في `app.py` هي `user`) و `is_active`. `init_db.py` ينشئ مستخدما باسم `admin` إن غاب. رسالة الطرفية في `init_db.py` تطبع كلمة مرور افتراضية. القيمة غير مكررة هنا.

## 4. ماذا يستطيع النظام أن يفعل؟

| الوظيفة | المسار | الحماية الظاهرة |
| --- | --- | --- |
| الصفحة الرئيسية | `GET /` | بلا `@login_required` |
| دخول وخروج | `/login` و `/logout` | عام |
| لوحة | `/dashboard` | `login_required` |
| تحليل | `/analyze` | `login_required` |
| رفع | `POST /upload` | `login_required` |
| سجل | `/history` | `login_required` |
| تفاصيل تحليل | `/analysis/<id>` | `login_required` |
| حذف تحليل | `POST /analysis/<id>/delete` | `login_required` |
| إحصاءات | `/statistics` و `GET /api/stats` | `login_required` |
| صورة نتيجة | `/result_image/<filename>` | المزخرف غير ظاهر بين المسار والدالة |
| ملف مرفوع | `/uploads/<path>` | المزخرف غير ظاهر بين المسار والدالة |

سكربتات جانبية: `train.py`, `evaluate.py`, `infer.py`, `prepare_yolo.py`, `add_sample_data.py`, `update_db.py`, `run_tests.py`, `init_db.py`.

## 5. كيف يعمل النظام؟

```
المتصفح
-> Flask app.py
-> جلسة بعد /login
-> رفع صورة إلى مجلد uploads
-> OncoVisionInference من infer.py ونموذج YOLO
-> جداول analysis_results و detections
-> قالب النتيجة وصورة في inference_results
```

`app.py` يحاول إنشاء `OncoVisionInference` ويضع `MODEL_LOADED`. عند فشل التحميل يبقى المحرك فارغا ويُطبع تحذير.

## 6. أمثلة واقعية

تحليل صورة بعد الدخول:

1. `GET /login` ثم إرسال النموذج.
2. `hash_password` يقارن SHA-256 مع `password_hash`.
3. الجلسة تحفظ `role`.
4. `POST /upload` يتحقق من الامتداد والحجم.
5. الاستنتاج يكتب `tumor_detected`, `num_detections`, `max_confidence`, `avg_confidence`, `processing_time`, `annotated_image_path`, `model_version`.
6. كل صندوق في `detections` مع `confidence` و `x_min`, `y_min`, `x_max`, `y_max`.
7. `/history` يعرض الصفوف، و`/statistics` تجمعها.

## 7. رحلة المستخدم

فتح `http://localhost:5000` حسب رسالة `app.py`. التسجيل في الواجهة: صفحة `login.html` للدخول. بعد النجاح: `dashboard.html` ثم `analyze.html` ثم سجل `history.html` أو تفصيل `analysis_detail.html`.

## 8. الوحدات والأقسام

| الوحدة | الملفات | الوظيفة |
| --- | --- | --- |
| الويب | `app.py` و `templates` | صفحات وحفظ |
| الاستنتاج | `infer.py` | تشغيل YOLO |
| التدريب | `train.py` و `prepare_yolo.py` و `data.yaml` | تجهيز وتدريب |
| التقييم | `evaluate.py` | تقييم النموذج |
| العينات | `add_sample_data.py` و `data\raw\sample` | عينات نصية صغيرة |
| الواجهة | `static\css`, `static\js\language.js`, `static\js\main.js` | تنسيق ولغة |
| أكاديمي | مجلد `الملفات الأكاديمية` | `التقرير` و `العرض التقديمي` و `لوحة العرض.pdf` |
| أوزان | `yolov8n.pt` | ملف أوزان موجود في الجذر |

## 9. الشركات والكيانات

كيان شركات متعدد غير موجود في الملفات الحالية.

## 10. الصلاحيات

عمود `role` موجود. المسارات المحمية تتحقق من الجلسة عبر `login_required` ولا تفحص قيمة `role` في الأسطر التي أُحصيت للمزخرف. فرق صلاحيات الطبيب والمدير داخل الصفحات غير موثق beyond وجود العمود.

## 11. الأتمتة وWorkflows

سير موافقات غير موجود في الملفات الحالية. التسلسل الآلي هو: رفع، استنتاج، إدراج، سجل `system_logs` عبر `log_system_event`.

## 12. التكامل بين الوحدات

`analysis_results.user_id` يشير إلى `users`. `detections.result_id` يشير إلى نتيجة. `system_logs.user_id` اختياري. ملفات الصور على القرص ومساراتها في الأعمدة.

## 13. المصطلحات

| المصطلح | المعنى في المشروع |
| --- | --- |
| tumor | اسم الصنف الوحيد في `data.yaml` (`nc: 1`) |
| YOLOv8 | مكتبة `ultralytics` في `requirements.txt` |
| confidence | ثقة الكشف في النتائج |
| annotated image | مسار الصورة بعد الرسم |
| WAL | `PRAGMA journal_mode=WAL` في `get_db_connection` |

## 14. الأسئلة الشائعة

| السؤال | الجواب |
| --- | --- |
| ما قاعدة البيانات؟ | ملف `oncovision.db` |
| ما الامتدادات؟ | `png`, `jpg`, `jpeg`, `bmp`, `tiff` |
| ما الحد؟ | 16 ميغابايت في `MAX_FILE_SIZE` |
| أين الأوزان؟ | `yolov8n.pt` في الجذر، ومجلد `models` و `runs` موجودان |
| هل يوجد ملفان لإعداد البيانات؟ | نعم: `data.yaml` في الجذر و `data\data.yaml` |

## 15. Architecture

```
templates + static
      |
      v
app.py (جلسة، رفع، صفحات)
      |
      +--> infer.py --> YOLO --> inference_results
      |
      +--> oncovision.db
```

## 16. Tech Stack

من `requirements.txt`: Flask 2.3.3، Werkzeug 2.3.7، Jinja2 3.1.2، ultralytics 8.0.196، torch>=1.9.0، torchvision>=0.10.0، opencv-python 4.8.1.78، numpy 1.24.3، Pillow 10.0.1، matplotlib 3.7.2، seaborn 0.12.2، PyYAML 6.0.1. الواجهة قوالب Jinja و CSS و JavaScript. القاعدة SQLite.

سطور roboflow و Flask-Login و Flask-WTF معلّقة في `requirements.txt` وغير مثبتة من هذا الملف.

## 17. Project Structure

```
OncoVision
├── app.py infer.py train.py evaluate.py
├── init_db.py update_db.py add_sample_data.py
├── prepare_yolo.py run_tests.py
├── requirements.txt data.yaml
├── oncovision.db yolov8n.pt
├── templates\   index, login, dashboard, analyze,
│                history, analysis_detail, statistics,
│                error, base
├── static\css static\js static\fonts
├── data\        data.yaml و raw\sample
├── uploads\ inference_results\ models\ runs\
└── الملفات الأكاديمية\
```

## 18. Frontend

قوالب Jinja تمتد من `base.html` حسب أسماء الملفات. صفحات متعددة وليست تطبيق صفحة واحدة. `static\js\language.js` ملف لغة كبير. `static\js\main.js` سلوك عام. `dark-theme.css` و `style.css` للتنسيق. تحميل التحليل عبر نماذج HTML إلى `/upload` و `/analyze`.

## 19. Backend

Flask في `app.py`. دوال: `allowed_file`, `get_db_connection`, `init_database`, `safe_db_operation`, `log_system_event`, `hash_password`, `verify_password`, `login_required`. الاستنتاج في `infer.py`. SQL مباشر عبر `sqlite3` بمعاملات ظاهرة في إدراج السجل.

## 20. Request Flow

```
المتصفح
-> POST /upload
-> login_required
-> حفظ الملف في uploads
-> محرك الاستنتاج
-> INSERT في analysis_results و detections
-> تحويل إلى صفحة النتيجة
```

## 21. Database

ملف `oncovision.db`. الجداول من فحص المخطط الحي (بلا صفوف):

| الجدول | الأعمدة |
| --- | --- |
| `users` | `id`, `username`, `password_hash`, `role`, `is_active`, `created_at`, `last_login` |
| `analysis_results` | `id`, `image_name`, `tumor_detected`, `num_detections`, `max_confidence`, `avg_confidence`, `processing_time`, `annotated_image_path`, `created_at`, `user_id`, `model_version` |
| `detections` | `id`, `result_id`, `confidence`, `x_min`, `y_min`, `x_max`, `y_max` |
| `system_logs` | `id`, `level`, `message`, `module`, `user_id`, `created_at` |

الاتصال: `timeout=30` و WAL و `busy_timeout` 30000. `init_db.py` و `update_db.py` يهيئان أو يحدثان القاعدة. بذور: مستخدم `admin` من `init_db.py`.

تعارض إعداد البيانات: `data.yaml` في الجذر يستخدم مسارا نسبيا `data/yolo_dataset`. `data\data.yaml` يستخدم مسارا مطلقا يبدأ بـ `C:\Users\TRSI\...`.

## 22. API

| Method | Path | الغرض | المصادقة |
| --- | --- | --- | --- |
| GET | `/api/stats` | إحصاءات JSON | `login_required` |
| POST | `/upload` | رفع وتحليل | `login_required` |
| GET | `/result_image/<filename>` | إرسال صورة نتيجة | المزخرف غير ظاهر |
| GET | `/uploads/<path>` | إرسال ملف مرفوع | المزخرف غير ظاهر |

باقي المسارات صفحات HTML.

## 23. Authentication & Authorization

`/login` يتحقق بـ SHA-256 عبر `hash_password` و `verify_password`. الجلسة مفتاحها `secrets.token_hex(32)` عند إقلاع `app.py`، فيتغير كل تشغيل. `login_required` يمنع الصفحات المعلّمة. الخروج في `/logout`.

## 24. Security

| البند | الواقع |
| --- | --- |
| تجزئة كلمة المرور | SHA-256 بلا ملح ظاهر في `hash_password` |
| اسم ملف الرفع | `werkzeug.utils.secure_filename` مستورد في `app.py` |
| حجم الرفع | 16 ميغابايت |
| امتدادات | القائمة في `ALLOWED_EXTENSIONS` |
| SQL | معاملات `?` في العمليات المفحوصة |
| CSRF | غير موجود في الملفات الحالية |
| وضع Flask | `debug=True` و `host='0.0.0.0'` والمنفذ 5000 |
| عرض الملفات | مسارا الصورة والرفع بلا `login_required` ظاهر |
| السجلات | `system_logs` |

## 25. Configuration

إعدادات داخل `app.py`: مجلدات `uploads` و `inference_results`، الامتدادات، الحجم، مفتاح الجلسة العشوائي. `data.yaml` و `data\data.yaml` لمسارات YOLO. متغيرات بيئة غير مستخدمة في `app.py` (قائمة `os.environ` فارغة عند الفحص).

## 26. Integrations

خدمة سحابية مفعّلة غير موجودة. سطر roboflow معلّق في المتطلبات. الواجهة محلية.

## 27. Scheduled Jobs

Cron أو عامل خلفية غير موجود في الملفات الحالية.

## 28. File Storage

الرفع إلى `uploads`. المخرجات إلى `inference_results`. الأوزان `yolov8n.pt`. عينات `data\raw\sample\sample_*.txt`. مجلدات `models` و `runs` موجودة.

## 29. Logging & Monitoring

`log_system_event` يدرج في `system_logs`. معالجات `not_found_error` و `internal_error` و `too_large` في `app.py`. مراقبة خارجية غير موجودة في الملفات الحالية.

## 30. Installation

```
pip install -r requirements.txt
python init_db.py
python app.py
```

ثم فتح العنوان الذي تطبعه الرسالة: `http://localhost:5000`. التدريب منفصل: `python train.py` بعد تجهيز `prepare_yolo.py` ومسارات `data.yaml`.

## 31. Development Guide

صفحة: قالب في `templates` ومسار في `app.py` مع `login_required` إن كانت خاصة. جدول: تعديل `init_database` في `app.py` و `init_db.py` معا حتى لا يفترقا. ميزة تحليل: `infer.py`. دور جديد: عمود `role` موجود بلا فحوص صفحات إضافية ظاهرة.

## 32. Deployment

`app.run(debug=True, host='0.0.0.0', port=5000)`. ملف إنتاج يطفئ debug غير موجود في الملفات الحالية. مفتاح الجلسة يتولد عند كل إقلاع.

## 33. Backup & Recovery

آلية نسخ غير موجودة في الملفات الحالية. الملفات الحافظة: `oncovision.db` و `uploads` و `inference_results` و `yolov8n.pt`.

## 34. Troubleshooting

| العرض | السبب الظاهر |
| --- | --- |
| النموذج غير محمّل | استثناء عند إنشاء `OncoVisionInference`، و`MODEL_LOADED` يصبح False |
| بيانات التدريب على مسار قديم | `data\data.yaml` يشير إلى مستخدم `TRSI` |
| الجلسة تسقط بعد إعادة التشغيل | `secret_key` عشوائي عند الإقلاع |
| ملف أكبر من الحد | `MAX_CONTENT_LENGTH` ومعالج الحجم |

## 35. Dependencies

مثبتة بأرقام في القسم 16. `torch` بحد أدنى فقط. اختبارات: `run_tests.py` موجود، وحزم pytest معلّقة في المتطلبات.

## 36. Known Limitations

- SHA-256 لكلمة المرور بلا ملح في الدالة الحالية.
- debug مفعّل.
- مسارات صور بلا مزخرف دخول ظاهر.
- ملفّا `data.yaml` غير متطابقين في المسار.
- README السابق يشرح `app.py` سطرا بسطر وقد يسبق تعديلا لاحقا؛ هذه الوثيقة تعتمد المسارات والجداول الحالية.
- الصنف الوحيد المعرّف: `tumor`.

## 37. Current System State

| البند | الحالة |
| --- | --- |
| تطبيق ويب وقالب وقاعدة | موجودة، و`oncovision.db` فيه الجداول الأربعة |
| أوزان yolov8n.pt | موجودة |
| مجموعة تدريب كاملة | المسار في الإعداد، واكتمال الصور غير موثق هنا |
| عينات raw | ملفات `sample_*.txt` صغيرة |
| مواد أكاديمية | ثلاثة أسماء مجلدات/ملفات تحت `الملفات الأكاديمية` |
| تشغيل أثناء الكتابة | غير موثق |

## 38. Architecture Decisions

- Flask مع قوالب متعددة الصفحات. الدليل: `templates` و `app.py`.
- SQLite بملف واحد ووضع WAL. الدليل: `get_db_connection`.
- YOLO لصنف واحد اسمه tumor. الدليل: `data.yaml`.
- جلسة Flask بدل Flask-Login. الدليل: الاستيراد الفعلي وتعليق الحزمة في المتطلبات.

## 39. سجل التغييرات

سجل إصدارات مستقل غير موجود في الملفات الحالية. `update_db.py` يحدّث مخطط القاعدة، وهذا سكربت تحديث وليس سجل نشر.

## System Overview

```
مستخدم -> /login -> جلسة
              -> /upload -> YOLO (tumor)
              -> oncovision.db
              -> /history و /statistics
```

## Quick Reference

| الجزء | التقنية | الموقع | الوظيفة |
| --- | --- | --- | --- |
| الويب | Flask | `app.py` | صفحات وAPI |
| الاستنتاج | ultralytics | `infer.py` | كشف |
| التدريب | Python | `train.py` | تدريب |
| البيانات | YAML | `data.yaml` | مسارات وصور |
| القاعدة | SQLite | `oncovision.db` | مستخدمون ونتائج |
| القوالب | Jinja | `templates` | الواجهة |
| اللغة | JavaScript | `static\js\language.js` | نصوص الواجهة |

## Quick Start

```
pip install -r requirements.txt
python init_db.py
python app.py
```

الدخول بالمستخدم الذي ينشئه `init_db.py`. غيّر كلمة المرور الظاهرة في رسالة ذلك الملف خارج هذه الوثيقة.

## For Non-Technical Users

الموقع يستقبل صورة ماموجرام ويحدد إن كان النموذج وجد منطقة مصنفة ورما، مع درجة ثقة. تحتاج إلى حساب للدخول. النتائج تبقى في السجل. الناتج مساعدة تحليلية حسب الكود، ووثيقة اعتماد سريري غير موجودة في الملفات الحالية.

## For Developers

- التقنيات: Flask 2.3.3 و Ultralytics 8.0.196 و PyTorch و OpenCV و SQLite.
- المعمارية: `app.py` يستدعي `infer.py` ويكتب SQLite.
- القاعدة: `users`, `analysis_results`, `detections`, `system_logs`.
- الواجهة الوحيدة بنمط API: `GET /api/stats` بالإضافة إلى `POST /upload`.
- ملفات مهمة: `app.py`, `infer.py`, `init_db.py`, `data.yaml`, `templates\analyze.html`.
- التطوير: أبقِ إنشاء الجداول في `app.py` و `init_db.py` متطابقا، ووحّد ملفي YAML.
