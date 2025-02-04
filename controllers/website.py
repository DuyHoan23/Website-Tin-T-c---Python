from odoo import http
from odoo.http import request

class WebsiteController(http.Controller):
    @http.route('/news/homepage', type='http', auth='public', website=True)
    def homepage(self):
        articles = http.request.env['newsinformation.newsinformation'].search([])
        categories = http.request.env['categoriesinformation.categoriesinformation'].search([])
        return http.request.render('news.homepage', {
            'articles': articles,
            'categories':categories,
        })

    @http.route('/news/<int:article_id>', type='http', auth='public', website=True)
    def article_detail(self, article_id):
        # Tìm bài báo theo ID
        article = request.env['newsinformation.newsinformation'].sudo().browse(article_id)
        categories = request.env['categoriesinformation.categoriesinformation'].search([])

        # Lấy tất cả các bình luận cho bài viết
        comments = request.env['commentinformation.commentinformation'].sudo().search([('new_id', '=', article_id)])

        # Kiểm tra nếu bài báo tồn tại
        if not article.exists():
            return request.not_found()  # Hiển thị trang lỗi 404 nếu không tìm thấy

        # Truyền dữ liệu bài báo, bình luận và người dùng vào template
        return request.render('news.article_detail', {
            'article': article,
            'categories': categories,
            'comments': comments,  # Danh sách bình luận
        })

    @http.route('/news/category/<int:category_id>', type='http', auth="public", website=True)
    def articles_by_category(self, category_id, **kwargs):
        # Lấy danh mục hiện tại
        category = http.request.env['categoriesinformation.categoriesinformation'].sudo().browse(category_id)
        categories = http.request.env['categoriesinformation.categoriesinformation'].search([])
        if not category.exists():
            return http.request.not_found()

        # Lấy các bài viết thuộc danh mục này
        articles = http.request.env['newsinformation.newsinformation'].sudo().search([('id_category', '=', category_id)])

        # Render template với danh sách bài viết
        return http.request.render('news.category_detail', {
            'categories': categories,
            'category': category,
            'articles': articles,
        })

    @http.route('/news/search', type='http', auth="public", website=True)
    def search_articles(self, query='', **kwargs):
        # Nếu không có từ khóa, trả về trang trống
        if not query:
            return http.request.render('news.search_results', {
                'query': query,
                'articles': [],
            })

        # Tìm kiếm bài viết theo tiêu đề hoặc nội dung
        articles = http.request.env['newsinformation.newsinformation'].sudo().search([
            '|',
            ('title', 'ilike', query),  # Tìm trong tiêu đề
            ('content', 'ilike', query)  # Tìm trong nội dung
        ])

        # Render template với kết quả
        return http.request.render('news.search_results', {
            'query': query,
            'articles': articles,
        })

    @http.route('/login', type='http', auth='public', website=True)
    def login_page(self, **kwargs):
        """Render trang đăng nhập."""
        return request.render('news.login_page', {})

    @http.route('/do_login', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def do_login(self, **post):
        """Xử lý logic đăng nhập."""
        email = post.get('email')
        password = post.get('password')
        articles = http.request.env['newsinformation.newsinformation'].search([])
        categories = http.request.env['categoriesinformation.categoriesinformation'].search([])
        # Kiểm tra thông tin đăng nhập
        user = request.env['userinformation.userinformation'].sudo().search([('email', '=', email)], limit=1)
        if user and user.sudo().check_password(password):
            # Thiết lập session
            request.session.uid = user.id
            return request.render('news.homepage', {
                'email': email,
                'articles': articles,
                'categories': categories,
            })
        else:
            # Đăng nhập thất bại
            return request.render('news.login_page', {
                'error': 'Email hoặc mật khẩu không chính xác.'
            })

    @http.route('/logout', type='http', auth='public', website=True)
    def logout(self, **kwargs):
        """Đăng xuất người dùng."""
        request.session.logout()
        return request.redirect('/login')

    @http.route('/register', auth='public', type='http', website=True)
    def register(self, **kw):
        return request.render('news.registration_form')

    @http.route('/submit_registration', auth='public', type='http', website=True, methods=['POST'], csrf=False)
    def submit_registration(self, **kw):
        # Lấy thông tin từ form đăng ký
        userName = kw.get('userName')
        email = kw.get('email')
        password = kw.get('password')

        # Kiểm tra và xử lý dữ liệu
        if userName and email and password:
            # Thực hiện tạo tài khoản người dùng mới
            user_obj = request.env['userinformation.userinformation']
            user_obj.sudo().create({
                'userName': userName,
                'email': email,
                'password': password,
            })
            return request.redirect('/login')
        else:
            return request.render('news.registration_failure', {'error': 'Thông tin không đầy đủ'})

    @http.route('/comment/submit/<int:id>', type='http', auth="public", methods=['POST'], csrf=False)
    def submit_comment(self, id, **kwargs):
        # Lấy dữ liệu từ form
        comment = kwargs.get('comment')
        user_id = request.session.uid
        # Kiểm tra nếu người dùng đã đăng nhập
        if not user_id:
            return request.redirect('/login')
        # Lưu dữ liệu vào model kèm ID bài viết
        request.env['commentinformation.commentinformation'].sudo().create({
            'user_id': user_id,
            'content': comment,
            'new_id': id,  # Liên kết với bài viết
        })
        request.session['success_message'] = "Bình luận đang được duyệt"
        return request.redirect(f'/news/{id}')

