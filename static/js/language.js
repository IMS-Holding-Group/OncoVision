// OncoVision - Bilingual Support System
class LanguageManager {
    constructor() {
        this.currentLang = localStorage.getItem('oncovision_lang') || 'ar';
        this.translations = {};
        this.init();
    }

    init() {
        this.loadTranslations();
        this.setupLanguageToggle();
        this.applyLanguage(this.currentLang);
    }

    loadTranslations() {
        this.translations = {
            ar: {
                // Dashboard
                'dashboard.title': 'لوحة التحكم',
                'dashboard.total_analyses': 'إجمالي التحاليل',
                'dashboard.tumor_detected': 'أورام مكتشفة',
                'dashboard.total_detections': 'إجمالي الاكتشافات',
                'dashboard.avg_confidence': 'متوسط الثقة',
                'dashboard.quick_actions': 'إجراءات سريعة',
                'dashboard.new_analysis': 'تحليل جديد',
                'dashboard.new_analysis.desc': 'قم برفع صورة ماموجرام جديدة للتحليل',
                'dashboard.view_history': 'عرض السجل',
                'dashboard.view_history.desc': 'استعرض جميع التحاليل السابقة',
                'dashboard.statistics': 'الإحصائيات',
                'dashboard.statistics.desc': 'عرض تقارير وإحصائيات مفصلة',
                'dashboard.recent_analyses': 'التحاليل الأخيرة',
                'dashboard.view_all': 'عرض الكل',
                'dashboard.image_name': 'اسم الصورة',
                'dashboard.date': 'التاريخ',
                'dashboard.result': 'النتيجة',
                'dashboard.detections_count': 'عدد الاكتشافات',
                'dashboard.max_confidence': 'أعلى ثقة',
                'dashboard.actions': 'الإجراءات',
                'dashboard.status.tumor': 'ورم مكتشف',
                'dashboard.status.normal': 'طبيعي',
                'dashboard.empty.title': 'لا توجد تحاليل بعد',
                'dashboard.empty.desc': 'ابدأ بتحليل أول صورة ماموجرام',
                'dashboard.start_analysis': 'بدء التحليل',
                'dashboard.welcome': 'مرحباً {name}، إليك ملخص نشاط النظام',
                // Navigation
                'nav.home': 'الرئيسية',
                'nav.analyze': 'تحليل',
                'nav.history': 'السجل',
                'nav.statistics': 'الإحصائيات',
                'nav.logout': 'تسجيل خروج',

                // Header
                'header.title': 'OncoVision - نظام كشف أورام الثدي',
                'header.subtitle': 'تحليل ذكي للماموجرام باستخدام الذكاء الاصطناعي',

                // Home Page
                'home.welcome': 'مرحبا بك في OncoVision',
                'home.description': 'نظام متقدم لكشف أورام الثدي باستخدام تقنيات الذكاء الاصطناعي والتعلم العميق',
                'home.features.title': 'المميزات الرئيسية',
                'home.features.ai': 'ذكاء اصطناعي متقدم',
                'home.features.ai.desc': 'خوارزميات YOLOv8 المتطورة لكشف الأورام بدقة عالية',
                'home.features.fast': 'تحليل سريع',
                'home.features.fast.desc': 'نتائج فورية خلال ثوانٍ معدودة',
                'home.features.accurate': 'دقة عالية',
                'home.features.accurate.desc': 'معدل دقة يصل إلى 95% في كشف الأورام',
                'home.features.secure': 'آمان تام',
                'home.features.secure.desc': 'حماية كاملة لبيانات المرضى والصور الطبية',
                'home.start.analysis': 'بدء التحليل',
                'home.view.history': 'عرض السجل',

                // Analysis Page
                'analysis.title': 'تحليل صورة الماموجرام',
                'analysis.upload.title': 'رفع صورة الماموجرام',
                'analysis.upload.description': 'اختر صورة ماموجرام عالية الجودة للتحليل',
                'analysis.upload.drag': 'اسحب الصورة هنا أو انقر للاختيار',
                'analysis.upload.formats': 'الصيغ المدعومة: JPG, PNG, DICOM',
                'analysis.upload.maxsize': 'الحد الأقصى: 10 ميجابايت',
                'analysis.analyze.btn': 'تحليل الصورة',
                'analysis.analyzing': 'جاري التحليل...',
                'analysis.settings.title': 'إعدادات التحليل',
                'analysis.settings.confidence': 'مستوى الثقة',
                'analysis.settings.confidence.desc': 'حدد الحد الأدنى لمستوى الثقة في النتائج',
                'analysis.settings.iou': 'IoU Threshold',
                'analysis.settings.iou.desc': 'حدد عتبة التداخل للكشف عن الأورام',
                'analysis.result.title': 'نتيجة التحليل',
                'analysis.result.confidence': 'مستوى الثقة',
                'analysis.result.detected': 'تم اكتشاف ورم',
                'analysis.result.normal': 'لا توجد أورام مكتشفة',
                'analysis.result.recommendation': 'التوصية الطبية',
                'analysis.result.consult': 'يُنصح بمراجعة طبيب مختص',
                'analysis.result.routine': 'فحص روتيني منتظم',
                'analysis.subtitle': 'رفع صورة طبية للحصول على تحليل دقيق باستخدام الذكاء الاصطناعي',
                'analysis.analyze': 'بدء التحليل',
                'analysis.save': 'حفظ النتائج',
                'analysis.results.title': 'نتائج التحليل',
                'nav.history': 'السجل',
                'nav.statistics': 'الإحصائيات',
                'nav.settings': 'الإعدادات',
                'settings.advanced.title': 'الإعدادات المتقدمة',
                'settings.model.title': 'إعدادات النموذج',
                'settings.model.type': 'نوع النموذج:',
                'settings.model.confidence': 'عتبة الثقة الافتراضية:',
                'settings.display.title': 'إعدادات العرض',
                'settings.display.confidence': 'عرض درجات الثقة',
                'settings.display.boxes': 'عرض المربعات المحيطة',
                'settings.display.labels': 'عرض التسميات',
                'settings.export.title': 'إعدادات التصدير',
                'settings.export.format': 'تنسيق التصدير:',
                'settings.export.auto': 'حفظ النتائج تلقائياً',
                'settings.save': 'حفظ الإعدادات',
                'settings.reset': 'إعادة تعيين',
                'history.title': 'سجل التحليلات',
                'stats.title': 'الإحصائيات والتقارير',
                // Detail Page
                'detail.title': 'تفاصيل التحليل',
                'detail.back': 'العودة للوحة التحكم',
                'detail.file.info': 'معلومات الملف',
                'detail.file.name': 'اسم الملف:',
                'detail.date': 'تاريخ التحليل:',
                'detail.processing': 'وقت المعالجة:',
                'detail.results': 'نتائج التحليل',
                'detail.tumor.status': 'حالة الورم:',
                'detail.detections.count': 'عدد الاكتشافات:',
                'detail.max.confidence': 'أعلى ثقة:',
                'detail.analyzed.image': 'الصورة المحللة',

                // History Page
                'history.title': 'سجل التحليلات',
                'history.new.analysis': 'تحليل جديد',
                'history.empty': 'لا توجد تحليلات سابقة',
                'history.date': 'التاريخ',
                'history.result': 'النتيجة',
                'history.confidence': 'مستوى الثقة',
                'history.actions': 'الإجراءات',
                'history.view': 'عرض',
                'history.delete': 'حذف',
                'history.export': 'تصدير',
                'history.filter.all': 'جميع النتائج',
                'history.filter.positive': 'إيجابية',
                'history.filter.negative': 'سلبية',
                'history.search.placeholder': 'البحث في السجل...',
                'history.page.prev': 'السابق',
                'history.page.next': 'التالي',
                'history.page.info': 'صفحة',

                // Statistics Page
                'stats.title': 'الإحصائيات والتقارير',
                'stats.subtitle': 'نظرة شاملة على أداء النظام ونتائج التحليلات',
                'stats.overview': 'نظرة عامة',
                'stats.total.analyses': 'إجمالي التحليلات',
                'stats.total.desc': 'جميع التحليلات المنجزة',
                'stats.positive.cases': 'الحالات الإيجابية',
                'stats.positive.desc': 'تحليلات اكتشفت أورام',
                'stats.positive.result': 'إيجابي',
                'stats.negative.cases': 'الحالات السليمة',
                'stats.negative.desc': 'تحليلات لم تكتشف أورام',
                'stats.negative.result': 'سلبي',
                'stats.accuracy.rate': 'معدل الدقة',
                'stats.monthly.trend': 'الاتجاه الشهري',
                'stats.detection.accuracy': 'دقة الكشف',
                'stats.processing.time': 'متوسط وقت المعالجة',
                'stats.processing.desc': 'الوقت المطلوب للتحليل',
                'stats.success.rate': 'معدل النجاح',
                'stats.success.desc': 'نسبة التحليلات المكتملة',
                'stats.avg.confidence': 'متوسط الثقة',
                'stats.avg.confidence.desc': 'مستوى الثقة في النتائج',
                'stats.export.report': 'تصدير التقرير',
                'stats.daily.analyses': 'التحليلات اليومية',
                'stats.daily.desc': 'عدد التحليلات المنجزة يومياً',
                'stats.results.distribution': 'توزيع النتائج',
                'stats.distribution.desc': 'نسبة الحالات الإيجابية والسلبية',
                'stats.recent.activity': 'النشاط الأخير',
                'stats.recent.desc': 'آخر التحليلات المنجزة',
                'stats.daily.summary': 'ملخص التحليلات اليومية',
                'stats.summary.title': 'ملخص التحليلات',
                'stats.summary.desc': 'إحصائيات مفصلة للتحليلات',
                'stats.date': 'التاريخ',
                'stats.analyses.count': 'عدد التحليلات',
                'stats.detection.rate': 'معدل الاكتشاف',
                'stats.tumor.detected': 'ورم محتمل',
                'stats.healthy': 'سليم',
                'stats.total': 'إجمالي',
                'stats.positive': 'إيجابي',
                'stats.negative': 'سلبي',
                'stats.no.data': 'لا توجد إحصائيات',
                'stats.no.data.desc': 'لم تقم بأي تحليلات بعد. ابدأ بتحليل صورة ماموجرام لرؤية الإحصائيات.',
                'stats.new.analysis': 'تحليل جديد',

                // Login Page
                'login.title': 'تسجيل الدخول',
                'login.subtitle': 'ادخل بياناتك للوصول إلى نظام OncoVision',
                'login.username': 'اسم المستخدم',
                'login.username.placeholder': 'ادخل اسم المستخدم',
                'login.password': 'كلمة المرور',
                'login.password.placeholder': 'ادخل كلمة المرور',
                'login.remember': 'تذكرني',
                'login.submit': 'تسجيل الدخول',
                'login.forgot': 'نسيت كلمة المرور؟',
                'login.system.title': 'نظام OncoVision',
                'login.system.description': 'نظام متطور لتحليل صور الماموجرام باستخدام الذكاء الاصطناعي',
                'login.features.security': 'أمان عالي للبيانات',
                'login.features.ai': 'ذكاء اصطناعي متقدم',
                'login.features.accuracy': 'دقة عالية في التشخيص',

                // Common
                'common.loading': 'جاري التحميل...',
                'common.error': 'حدث خطأ',
                'common.success': 'تم بنجاح',
                'common.warning': 'تحذير',
                'common.info': 'معلومة',
                'common.cancel': 'إلغاء',
                'common.confirm': 'تأكيد',
                'common.save': 'حفظ',
                'common.edit': 'تعديل',
                'common.delete': 'حذف',
                'common.close': 'إغلاق',
                'common.back': 'رجوع',
                'common.next': 'التالي',
                'common.previous': 'السابق',
                'common.search': 'بحث',
                'common.filter': 'تصفية',
                'common.export': 'تصدير',
                'common.print': 'طباعة',
                'common.download': 'تحميل',
                'common.upload': 'رفع',
                'common.select': 'اختيار',
                'common.clear': 'مسح',
                'common.refresh': 'تحديث',

                // Footer
                'footer.copyright': '© 2025 OncoVision. جميع الحقوق محفوظة.',
                'footer.privacy': 'سياسة الخصوصية',
                'footer.terms': 'شروط الاستخدام',
                'footer.contact': 'اتصل بنا',
                'footer.about': 'حول النظام',

                // Error Messages
                'error.file.size': 'حجم الملف كبير جداً',
                'error.file.format': 'صيغة الملف غير مدعومة',
                'error.upload.failed': 'فشل في رفع الملف',
                'error.analysis.failed': 'فشل في تحليل الصورة',
                'error.network': 'خطأ في الاتصال',
                'error.server': 'خطأ في الخادم',
                'error.unauthorized': 'غير مصرح لك بالوصول',
                'error.not.found': 'الصفحة غير موجودة',

                // Success Messages
                'success.upload': 'تم رفع الملف بنجاح',
                'success.analysis': 'تم التحليل بنجاح',
                'success.save': 'تم الحفظ بنجاح',
                'success.delete': 'تم الحذف بنجاح',
                'success.export': 'تم التصدير بنجاح',

                // Medical Disclaimer
                'disclaimer.title': 'إخلاء مسؤولية طبية',
                'disclaimer.content': 'هذا النظام مخصص للمساعدة في التشخيص فقط وليس بديلاً عن الاستشارة الطبية المتخصصة. جميع النتائج يجب أن تُراجع من قبل طبيب مختص. لا يتحمل النظام أي مسؤولية عن القرارات الطبية المتخذة بناءً على هذه النتائج.',
                'disclaimer.understand': 'أفهم وأوافق'
            },

            en: {
                // Dashboard
                'dashboard.title': 'Dashboard',
                'dashboard.total_analyses': 'Total Analyses',
                'dashboard.tumor_detected': 'Tumors Detected',
                'dashboard.total_detections': 'Total Detections',
                'dashboard.avg_confidence': 'Average Confidence',
                'dashboard.quick_actions': 'Quick Actions',
                'dashboard.new_analysis': 'New Analysis',
                'dashboard.new_analysis.desc': 'Upload a new mammogram image for analysis',
                'dashboard.view_history': 'View History',
                'dashboard.view_history.desc': 'Browse all previous analyses',
                'dashboard.statistics': 'Statistics',
                'dashboard.statistics.desc': 'View detailed reports and statistics',
                'dashboard.recent_analyses': 'Recent Analyses',
                'dashboard.view_all': 'View All',
                'dashboard.image_name': 'Image Name',
                'dashboard.date': 'Date',
                'dashboard.result': 'Result',
                'dashboard.detections_count': 'Detections Count',
                'dashboard.max_confidence': 'Max Confidence',
                'dashboard.actions': 'Actions',
                'dashboard.status.tumor': 'Tumor Detected',
                'dashboard.status.normal': 'Normal',
                'dashboard.empty.title': 'No analyses yet',
                'dashboard.empty.desc': 'Start by analyzing your first mammogram image',
                'dashboard.start_analysis': 'Start Analysis',
                'dashboard.welcome': 'Welcome {name}, here is your system activity summary',
                // Navigation
                'nav.home': 'Home',
                'nav.analyze': 'Analyze',
                'nav.history': 'History',
                'nav.statistics': 'Statistics',
                'nav.logout': 'Logout',

                // Header
                'header.title': 'OncoVision - Breast Cancer Detection System',
                'header.subtitle': 'AI-Powered Mammogram Analysis',

                // Home Page
                'home.welcome': 'Welcome to OncoVision',
                'home.description': 'Advanced breast cancer detection system using artificial intelligence and deep learning technologies',
                'home.features.title': 'Key Features',
                'home.features.ai': 'Advanced AI',
                'home.features.ai.desc': 'State-of-the-art YOLOv8 algorithms for high-precision tumor detection',
                'home.features.fast': 'Fast Analysis',
                'home.features.fast.desc': 'Instant results within seconds',
                'home.features.accurate': 'High Accuracy',
                'home.features.accurate.desc': 'Up to 95% accuracy rate in tumor detection',
                'home.features.secure': 'Secure',
                'home.features.secure.desc': 'Complete protection of patient data and medical images',
                'home.start.analysis': 'Start Analysis',
                'home.view.history': 'View History',

                // Analysis Page
                'analysis.title': 'Mammogram Analysis',
                'analysis.upload.title': 'Upload Mammogram Image',
                'analysis.upload.description': 'Select a high-quality mammogram image for analysis',
                'analysis.upload.drag': 'Drag image here or click to select',
                'analysis.upload.formats': 'Supported formats: JPG, PNG, DICOM',
                'analysis.upload.maxsize': 'Maximum size: 10 MB',
                'analysis.analyze.btn': 'Analyze Image',
                'analysis.analyzing': 'Analyzing...',
                'analysis.settings.title': 'Analysis Settings',
                'analysis.settings.confidence': 'Confidence Level',
                'analysis.settings.confidence.desc': 'Set the minimum confidence level for results',
                'analysis.settings.iou': 'IoU Threshold',
                'analysis.settings.iou.desc': 'Set the intersection threshold for tumor detection',
                'analysis.result.title': 'Analysis Result',
                'analysis.result.confidence': 'Confidence Level',
                'analysis.result.detected': 'Tumor Detected',
                'analysis.result.normal': 'No Tumors Detected',
                'analysis.result.recommendation': 'Medical Recommendation',
                'analysis.result.consult': 'Consult with a specialist',
                'analysis.result.routine': 'Regular routine checkup',
                'analysis.subtitle': 'Upload a medical image for accurate analysis using artificial intelligence',
                'analysis.analyze': 'Start Analysis',
                'analysis.save': 'Save Results',
                'analysis.results.title': 'Analysis Results',
                'nav.history': 'History',
                'nav.statistics': 'Statistics',
                'nav.settings': 'Settings',
                'settings.advanced.title': 'Advanced Settings',
                'settings.model.title': 'Model Settings',
                'settings.model.type': 'Model Type:',
                'settings.model.confidence': 'Default Confidence Threshold:',
                'settings.display.title': 'Display Settings',
                'settings.display.confidence': 'Show Confidence Scores',
                'settings.display.boxes': 'Show Bounding Boxes',
                'settings.display.labels': 'Show Labels',
                'settings.export.title': 'Export Settings',
                'settings.export.format': 'Export Format:',
                'settings.export.auto': 'Auto-save Results',
                'settings.save': 'Save Settings',
                'settings.reset': 'Reset',
                'history.title': 'Analysis History',
                'stats.title': 'Statistics and Reports',
                // Detail Page
                'detail.title': 'Analysis Details',
                'detail.back': 'Back to Dashboard',
                'detail.file.info': 'File Information',
                'detail.file.name': 'File Name:',
                'detail.date': 'Analysis Date:',
                'detail.processing': 'Processing Time:',
                'detail.results': 'Analysis Results',
                'detail.tumor.status': 'Tumor Status:',
                'detail.detections.count': 'Detections Count:',
                'detail.max.confidence': 'Max Confidence:',
                'detail.analyzed.image': 'Analyzed Image',

                // History Page
                'history.title': 'Analysis History',
                'history.new.analysis': 'New Analysis',
                'history.empty': 'No previous analyses',
                'history.date': 'Date',
                'history.result': 'Result',
                'history.confidence': 'Confidence',
                'history.actions': 'Actions',
                'history.view': 'View',
                'history.delete': 'Delete',
                'history.export': 'Export',
                'history.filter.all': 'All Results',
                'history.filter.positive': 'Positive',
                'history.filter.negative': 'Negative',
                'history.search.placeholder': 'Search history...',
                'history.page.prev': 'Previous',
                'history.page.next': 'Next',
                'history.page.info': 'Page',

                // Statistics Page
                'stats.title': 'Statistics & Reports',
                'stats.subtitle': 'Comprehensive overview of system performance and analysis results',
                'stats.overview': 'Overview',
                'stats.total.analyses': 'Total Analyses',
                'stats.total.desc': 'All completed analyses',
                'stats.positive.cases': 'Positive Cases',
                'stats.positive.desc': 'Analyses that detected tumors',
                'stats.positive.result': 'Positive',
                'stats.negative.cases': 'Healthy Cases',
                'stats.negative.desc': 'Analyses that found no tumors',
                'stats.negative.result': 'Negative',
                'stats.accuracy.rate': 'Accuracy Rate',
                'stats.monthly.trend': 'Monthly Trend',
                'stats.detection.accuracy': 'Detection Accuracy',
                'stats.processing.time': 'Average Processing Time',
                'stats.processing.desc': 'Time required for analysis',
                'stats.success.rate': 'Success Rate',
                'stats.success.desc': 'Percentage of completed analyses',
                'stats.avg.confidence': 'Average Confidence',
                'stats.avg.confidence.desc': 'Confidence level in results',
                'stats.export.report': 'Export Report',
                'stats.daily.analyses': 'Daily Analyses',
                'stats.daily.desc': 'Number of analyses completed daily',
                'stats.results.distribution': 'Results Distribution',
                'stats.distribution.desc': 'Ratio of positive and negative cases',
                'stats.recent.activity': 'Recent Activity',
                'stats.recent.desc': 'Latest completed analyses',
                'stats.daily.summary': 'Daily Analysis Summary',
                'stats.summary.title': 'Analysis Summary',
                'stats.summary.desc': 'Detailed analysis statistics',
                'stats.date': 'Date',
                'stats.analyses.count': 'Analysis Count',
                'stats.detection.rate': 'Detection Rate',
                'stats.tumor.detected': 'Tumor Detected',
                'stats.healthy': 'Healthy',
                'stats.total': 'Total',
                'stats.positive': 'Positive',
                'stats.negative': 'Negative',
                'stats.no.data': 'No Statistics Available',
                'stats.no.data.desc': 'You haven\'t performed any analyses yet. Start by analyzing a mammogram image to see statistics.',
                'stats.new.analysis': 'New Analysis',

                // Login Page
                'login.title': 'Login',
                'login.subtitle': 'Enter your credentials to access OncoVision system',
                'login.username': 'Username',
                'login.username.placeholder': 'Enter username',
                'login.password': 'Password',
                'login.password.placeholder': 'Enter password',
                'login.remember': 'Remember me',
                'login.submit': 'Login',
                'login.forgot': 'Forgot password?',
                'login.system.title': 'OncoVision System',
                'login.system.description': 'Advanced mammogram analysis system using artificial intelligence',
                'login.features.security': 'High Data Security',
                'login.features.ai': 'Advanced AI Technology',
                'login.features.accuracy': 'High Diagnostic Accuracy',

                // Common
                'common.loading': 'Loading...',
                'common.error': 'Error',
                'common.success': 'Success',
                'common.warning': 'Warning',
                'common.info': 'Info',
                'common.cancel': 'Cancel',
                'common.confirm': 'Confirm',
                'common.save': 'Save',
                'common.edit': 'Edit',
                'common.delete': 'Delete',
                'common.close': 'Close',
                'common.back': 'Back',
                'common.next': 'Next',
                'common.previous': 'Previous',
                'common.search': 'Search',
                'common.filter': 'Filter',
                'common.export': 'Export',
                'common.print': 'Print',
                'common.download': 'Download',
                'common.upload': 'Upload',
                'common.select': 'Select',
                'common.clear': 'Clear',
                'common.refresh': 'Refresh',

                // Footer
                'footer.copyright': '© 2025 OncoVision. All rights reserved.',
                'footer.privacy': 'Privacy Policy',
                'footer.terms': 'Terms of Use',
                'footer.contact': 'Contact Us',
                'footer.about': 'About System',

                // Error Messages
                'error.file.size': 'File size too large',
                'error.file.format': 'Unsupported file format',
                'error.upload.failed': 'File upload failed',
                'error.analysis.failed': 'Image analysis failed',
                'error.network': 'Network error',
                'error.server': 'Server error',
                'error.unauthorized': 'Unauthorized access',
                'error.not.found': 'Page not found',

                // Success Messages
                'success.upload': 'File uploaded successfully',
                'success.analysis': 'Analysis completed successfully',
                'success.save': 'Saved successfully',
                'success.delete': 'Deleted successfully',
                'success.export': 'Exported successfully',

                // Statistics
                'stats.title': 'Statistics & Reports',
                'stats.total.analyses': 'Total Analyses',
                'stats.positive.cases': 'Positive Cases',
                'stats.negative.cases': 'Negative Cases',
                'stats.processing.time': 'Average Processing Time',
                'stats.daily.analyses': 'Daily Analyses',
                'stats.results.distribution': 'Results Distribution',
                'stats.recent.activity': 'Recent Activity',
                'stats.tumor.detected': 'Tumor Detected',
                'stats.healthy': 'Healthy',
                'stats.daily.summary': 'Daily Analysis Summary',
                'stats.date': 'Date',
                'stats.analyses.count': 'Analysis Count',
                'stats.detection.rate': 'Detection Rate',
                'stats.no.data': 'No Statistics Available',
                'stats.no.data.desc': 'You haven\'t performed any analyses yet. Start by analyzing a mammogram image to see statistics.',
                'stats.new.analysis': 'New Analysis',

                // Medical Disclaimer
                'disclaimer.title': 'Medical Disclaimer',
                'disclaimer.content': 'This system is designed to assist in diagnosis only and is not a substitute for professional medical consultation. All results must be reviewed by a qualified physician. The system assumes no responsibility for medical decisions made based on these results.',
                'disclaimer.understand': 'I Understand and Agree'
            }
        };
    }

    setupLanguageToggle() {
        const langToggle = document.querySelector('.language-toggle');
        const langBtns = document.querySelectorAll('.lang-btn');
        const toggleBg = document.querySelector('.lang-toggle-bg');

        if (langBtns.length > 0) {
            langBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const lang = e.target.dataset.lang;
                    this.switchLanguage(lang);
                });
            });
        }
    }

    switchLanguage(lang) {
        if (lang === this.currentLang) return;

        this.currentLang = lang;
        localStorage.setItem('oncovision_lang', lang);
        this.applyLanguage(lang);

        // Update toggle UI
        this.updateToggleUI();

        // Trigger custom event for other components
        window.dispatchEvent(new CustomEvent('languageChanged', {
            detail: { language: lang }
        }));
    }

    applyLanguage(lang) {
        // Set document direction and class
        document.body.className = document.body.className.replace(/\b(rtl|ltr)\b/g, '');
        document.body.classList.add(lang === 'ar' ? 'rtl' : 'ltr');
        document.documentElement.setAttribute('lang', lang);
        document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');

        // Update all translatable elements
        this.updateTranslatableElements();

        // Update form placeholders
        this.updatePlaceholders();

        // Update dynamic content
        this.updateDynamicContent();
    }

    updateTranslatableElements() {
        const elements = document.querySelectorAll('[data-translate]');
        elements.forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.getTranslation(key);

            if (translation) {
                if (element.tagName === 'INPUT' && element.type === 'submit') {
                    element.value = translation;
                } else {
                    element.textContent = translation;
                }
            }
        });
    }

    updatePlaceholders() {
        const elements = document.querySelectorAll('[data-translate-placeholder]');
        elements.forEach(element => {
            const key = element.getAttribute('data-translate-placeholder');
            const translation = this.getTranslation(key);

            if (translation) {
                element.placeholder = translation;
            }
        });
    }

    updateDynamicContent() {
        // Update page title
        const titleKey = document.querySelector('meta[name="page-title"]');
        if (titleKey) {
            const key = titleKey.getAttribute('content');
            const translation = this.getTranslation(key);
            if (translation) {
                document.title = `${translation} - OncoVision`;
            }
        }

        // Update navigation active states
        this.updateNavigationStates();
    }

    updateNavigationStates() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link');

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }

    updateToggleUI() {
        const langBtns = document.querySelectorAll('.lang-btn');
        const toggleBg = document.querySelector('.lang-toggle-bg');

        langBtns.forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.lang === this.currentLang) {
                btn.classList.add('active');
            }
        });

        if (toggleBg) {
            toggleBg.className = `lang-toggle-bg ${this.currentLang}`;
        }
    }

    getTranslation(key) {
        return this.translations[this.currentLang]?.[key] || key;
    }

    translate(key, params = {}) {
        let translation = this.getTranslation(key);

        // Replace parameters in translation
        Object.keys(params).forEach(param => {
            translation = translation.replace(`{${param}}`, params[param]);
        });

        return translation;
    }

    getCurrentLanguage() {
        return this.currentLang;
    }

    isRTL() {
        return this.currentLang === 'ar';
    }

    // Format numbers based on language
    formatNumber(number) {
        if (this.currentLang === 'ar') {
            return new Intl.NumberFormat('ar-SA').format(number);
        }
        return new Intl.NumberFormat('en-US').format(number);
    }

    // Format dates based on language
    formatDate(date, options = {}) {
        const defaultOptions = {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        };

        const formatOptions = { ...defaultOptions, ...options };

        if (this.currentLang === 'ar') {
            return new Intl.DateTimeFormat('ar-SA', formatOptions).format(date);
        }
        return new Intl.DateTimeFormat('en-US', formatOptions).format(date);
    }
}

// Initialize language manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.languageManager = new LanguageManager();

    // Add smooth transitions for language changes
    document.body.style.transition = 'all 0.3s ease-in-out';
});

// Utility functions for easy access
window.translate = (key, params) => {
    return window.languageManager ? window.languageManager.translate(key, params) : key;
};

window.getCurrentLanguage = () => {
    return window.languageManager ? window.languageManager.getCurrentLanguage() : 'ar';
};

window.isRTL = () => {
    return window.languageManager ? window.languageManager.isRTL() : true;
};
