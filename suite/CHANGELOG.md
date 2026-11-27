# Changelog

Mọi thay đổi của Suite design system, mới nhất ở trên. Ghi thay đổi vào **Unreleased** khi làm, chia theo *Breaking*, *Added*, *Changed*, *Deprecated*, *Fixed*.

## [Unreleased]

## [0.4.1] — 2026-11-27

Thanh tab ở đáy và topbar gọn cho điện thoại, dùng được ở mọi vùng, không chỉ cổng tự phục vụ.

### Added
- `button.s-bottom-nav__more`: mục "Thêm" mở drawer. Khi có nút này, nút ☰ trên topbar tự ẩn dưới 768px.
- `.s-count` trong thanh tab nằm ở góc icon.
- `.s-user-menu`: nút avatar ở cuối topbar (avatar và tên từ 768px, chỉ avatar khi hẹp hơn), và `.s-menu__head` (dòng avatar, tên, email trong menu).
- `.s-topbar__back`: nút quay lại ở trang chi tiết, dưới 1024px, thay chỗ của ☰.
- Demo: shell thường (không còn tự phục vụ) có thanh tab 5 mục, mục "Thêm" và menu tài khoản.

### Changed
- `.s-bottom-nav` hiện ở mọi `.s-shell` dưới 768px, không còn cần `.s-shell--self-service`.
- Thanh tab chừa chỗ cho nội dung, và `.s-page-actions` nằm trên thanh tab, cho mọi shell có thanh tab.
- Mục của thanh tab có thể là `<a>` hoặc `<button>`. Nhãn dài bị cắt bằng dấu "…".

### Fixed
- `.s-pill-track` (0.4.0) ghi đè `position: fixed` của thanh tab ở đáy khi thanh tab có pill. Giờ rule này có độ ưu tiên 0 (`:where()`).

## [0.4.0] — 2026-11-27

Điều hướng có cấu trúc, component cây và danh sách, và lớp chuyển động chuyển từ Halvo.

### Added
- **Điều hướng:**
  - `.s-nav` và `.s-nav-section`: sidebar chia vùng Chung / Workspace / Cài đặt, luôn hiện đủ các vùng.
  - `.s-nav-item__label`, `.s-sidebar__foot`.
  - `.s-switcher` (bộ chuyển sản phẩm), `.s-product-tile` (theo `data-product`).
  - `.s-shell--rail`: sidebar chỉ có icon trên desktop.
- **Cây và danh sách:**
  - `.s-list`: hàng gồm lead, text, meta và chevron; có trạng thái đang chọn; biến thể `--divided`.
  - `.s-tree`: thụt lề theo `--level`, nút mở/đóng xoay, trạng thái đang chọn.
  - `.s-split`: bố cục master-detail, cột trái dính khi cuộn từ 1024px.
- **Chuyển động** (`components/motion.css`, `dist/motion.mjs` / `motion.js`, export `@suite/design-system/motion`):
  - `.s-motion-rise`, `.s-motion-slide`, `.s-motion-fade`, `.s-lift`, `.s-flash`.
  - Popover và menu bật ra.
  - Pill trượt cho tab, segmented, sidebar và thanh tab ở đáy (`pill()`, dùng `@property` để cạnh trước đi trước, cạnh sau đuổi theo như Halvo).
  - Số đếm lên (`countTo()`), `replay()`.
  - Chuyển trang bằng View Transitions (chỉ `.s-content` di chuyển).
- Token chuyển động lấy từ Halvo: `--ease-expo`, `--ease-power3`, `--ease-inout`, `--ease-spring`, `--dur-reveal`, `--stagger`. Đổi `--ease-in` sang đường cong power2.in của Halvo.
- Select: `button.s-select` cùng `.s-select__value`, `.s-select__placeholder`, và trạng thái mở (`aria-expanded`).

### Fixed
- `.s-select` dạng `<button>` bị canh chữ giữa. Giờ canh trái như input.
- `.s-page-actions` (từ 0.3.1) không dính được đáy màn hình trên điện thoại, vì `position: sticky` nằm trong page head. Giờ là thanh nổi `position: fixed` có kính, và vùng nội dung được chừa chỗ ở dưới. Ở cổng tự phục vụ, thanh này nằm phía trên thanh tab ở đáy.

## [0.3.1] — 2026-11-27

### Added
- `.s-pager__pages` và `.s-pager__more`: số trang hiện từ 768px, nút xem thêm khi hẹp hơn.
- `.s-page-actions`: hàng nút của page head. Dưới 768px hàng này dính đáy và chừa `safe-area`.

## [0.3.0] — 2026-11-27

Theme mặc định chuyển sang ngôn ngữ thiết kế Halvo. Suite trở thành nền để dựng design system cho từng khách hàng: mỗi khách hàng là một theme, và theme chọn một style preset.

### Breaking (cho app đang dùng 0.2.0)
- `themes/default` giờ là kính, mặc định tối. Giao diện phẳng cũ nay là theme `classic`. Deployment muốn giữ giao diện cũ thì đổi `Branding:ThemeId` sang `classic`.
- Theme không còn tự theo `prefers-color-scheme`. Không đặt `data-theme` thì dùng `defaultMode` của theme. Khi user chọn "Theo hệ thống", `ThemeService` phải tự đặt `data-theme` theo `matchMedia`.
- `civic` và `evergreen` kế thừa `classic` / `default` thay cho `default` cũ.

### Added
- Hợp đồng token bản 2:
  - Token màu mới: `surface-glass`, `surface-raised`, `rim`, `rim-2`, `primary-hi`, `glow`.
  - Paint `backdrop` (nền trang) và `primary-fill` (nền nút chính, mặc định là gradient ở kiểu kính).
  - Theme token `radius-xl`, `blur`, `blur-overlay`.
  - 30 **component token**: sidebar, topbar, card, nút, input, tab, mục menu, header bảng, badge.
  - Một số token màu được phép có alpha. Tương phản được đo sau khi chồng màu lên "ground" của token đó. Riêng kính được đo trên từng màu lấy từ `backdrop`.
- Style preset `flat` và `glass` trong `tokens/base.json`. Theme chọn preset bằng `style`, và có thể ghi đè từng component token trong `components`.
- Theme `classic` (phẳng). `evergreen` thành mẫu kính dựng từ `default` chỉ bằng màu thương hiệu.
- `new-theme` nhận thêm `--style`, `--mode`, `--extends`. Lệnh tự suy ra thêm `primary-hi`, `glow` và `primary-fill`.
- `.s-auth`: layout trang đăng nhập (card ở giữa, logo, form một cột, nút submit rộng hết card, link cạnh label).
- `.s-card--glass`, `.s-glass`, `.s-section-label`, `.s-field__row`, `.s-form-actions`, `.s-page-head__eyebrow`, `.s-brand__text`, `.s-launcher__icon`.
- `prefers-reduced-transparency`: kính thành đặc.

### Changed
- Khung ứng dụng: sidebar và topbar nổi, cách mép `--shell-inset`, bo `radius-xl` / `radius-lg`, có kính. Thanh tab ở đáy trên điện thoại nổi, mục đang chọn là pill màu thương hiệu.
- Nút cao 42px, nút chính có gradient và quầng sáng. Input cao 44px, focus có vòng sáng. Tab dạng pill trong một dải kính. Mục sidebar đang chọn có nền kính. Badge dạng pill. KPI có quầng màu ở góc.
- Dialog, drawer, menu, popover, toast dùng `surface-raised` với blur. Dialog bo `radius-xl`, và có tay nắm khi thành bottom sheet.
- Header bảng trong suốt ở kiểu kính. Cột đầu dính trái tô màu card bên dưới để nội dung cuộn không lộ qua.
- Dải màu workspace trên topbar chỉ hiện khi có `data-product`.

## [0.2.0] — 2026-11-26

### Added
- `s-popover` và `s-listbox`: option, option đang active, option đã chọn, nhóm, trạng thái loading và empty.
- `s-calendar`: lưới tháng (hôm nay, đã chọn, trong khoảng, vô hiệu, ngày nghỉ) và dạng agenda khi hẹp hơn 768px.
- `s-dropzone` và `s-file-list`: vùng kéo thả, tiến trình và lỗi.
- `s-stepper`: dạng ngang, và dạng "Bước n/N" khi hẹp.
- `s-filter-bar` và `s-chip`: bộ lọc đang áp dụng, có nút xóa. Dưới 768px chỉ còn ô tìm kiếm và nút mở bộ lọc.
- `s-tooltip`, `s-timeline`, `s-launcher`.
- Bảng: `.is-hide-stack` ẩn ô khi dạng thẻ, ẩn cột theo `data-priority` bằng container query, cột chọn dòng.

## [0.1.0] — 2026-11-26

Bản mẫu đầu tiên.

### Added
- Hợp đồng token `tokens/contract.json`: 40 màu, 3 bóng (theo chế độ sáng/tối), 5 token theme (font, bo góc), danh sách token admin khách hàng được đổi, 35 cặp tương phản phải đạt.
- Token cố định `tokens/base.json`: thang chữ, khoảng cách, chuyển động, z-index, 2 mức mật độ, danh sách font hỗ trợ tiếng Việt.
- 3 theme: `default`, `evergreen` (mẫu), `civic` (mẫu).
- `tools/build.mjs`: build `dist/`, kiểm tra theme, lệnh `new-theme` suy ra màu từ màu thương hiệu.
- CSS component tiền tố `s-`: button, form (input, select, textarea, checkbox, radio, switch, form grid), card, KPI, description list, badge, avatar, alert, banner, tabs, segmented, table (tự xếp thành thẻ khi hẹp), dialog và bottom sheet, drawer, menu, toast, app shell (sidebar, topbar, bottom nav), empty, skeleton, progress.
- Trang demo `demo/index.html`.
