# Suite design system

Design system cho **Business Suite** (CRM, ERP, HRM, DMS, BI, Workflow): giao diện nghiệp vụ nhiều dữ liệu, dùng cả ngày, chạy trên desktop lẫn điện thoại.

Theme mặc định được **dựng từ Halvo**:
- kính đặt trên nền có chiều sâu;
- một màu teal cho thứ đang bật hoặc cho hành động chính;
- bo góc lớn, lồng nhau;
- sidebar và topbar nổi cách mép màn hình;
- mặc định chế độ tối.

Suite là **nền để dựng các design system khác** cho từng khách hàng. Mỗi khách hàng là một theme (có thể chọn kiểu kính hoặc phẳng), dùng chung một bộ CSS component, và đổi theme không cần build lại ứng dụng.

> Bản 0.3.0. Chưa có công cụ release như `halvo/tools/release.py`.

## 1. Bốn tầng

| Tầng | Ai sửa | Gồm gì | Ở đâu |
|---|---|---|---|
| **Core** | Team design system | Hợp đồng token, thang chữ, khoảng cách, mật độ, chuyển động, CSS component | `tokens/contract.json`, `tokens/base.json` (`tokens`, `density`), `components/` |
| **Style preset** | Team design system | Cách các component trông ra sao: kính hay phẳng, sidebar nổi hay dính mép, tab dạng pill hay gạch chân… Mỗi preset là một bộ giá trị **component token** | `tokens/base.json → styles` (`flat`, `glass`) |
| **Theme** | Vendor, cho từng khách hàng | Chọn preset (`style`), chế độ mặc định (`defaultMode`), màu cho cả 2 chế độ, nền trang (`backdrop`), font, bo góc, blur, mật độ. Có thể ghi đè từng component token | `themes/<id>.json` → `dist/themes/<id>.css` |
| **Brand** | Admin của khách hàng, trên màn hình branding (làm sau) | `brand.primary`, `brand.accent`, bo góc, font | Dữ liệu tenant |

Muốn có một "design system khác", **thường chỉ cần tạo theme mới**. Cần một kiểu giao diện hoàn toàn mới (ví dụ viền đậm kiểu "brutal", hay bo tròn kiểu "soft") thì **thêm một style preset**. Cả hai cách đều **không** sửa CSS component, nên app không phải đổi gì.

Theme có sẵn:

| Theme | Style | Mặc định | Ghi chú |
|---|---|---|---|
| `default` | glass | tối | Halvo. Theme gốc của mọi theme kính |
| `evergreen` | glass | tối | Mẫu: kế thừa `default`, chỉ đổi màu thương hiệu, font, bo góc. Màu còn lại được suy ra |
| `classic` | flat | sáng | Phẳng, xanh dương. Theme gốc của mọi theme phẳng |
| `civic` | flat | sáng | Mẫu khối hành chính: navy, góc gần vuông, mật độ dày, Noto Sans |

## 2. Cấu trúc

```
suite/
├─ package.json            @suite/design-system, version
├─ tokens/
│  ├─ contract.json        token bắt buộc (màu, paint, bóng, theme, component) + cặp tương phản phải đạt + "ground" để chồng alpha
│  └─ base.json            token cố định, mật độ, font cho phép, style preset (flat, glass)
├─ themes/*.json           default, evergreen (kính) · classic, civic (phẳng)
├─ components/*.css        CSS component, tiền tố s- (s-btn, s-input, s-table, s-auth…), chỉ dùng token
├─ tools/
│  ├─ build.mjs            build + kiểm tra + lệnh new-theme (Node, không cần cài package)
│  └─ color.mjs            OKLCH, tương phản WCAG, suy ra màu từ màu thương hiệu
├─ demo/index.html         trang xem trước: đổi theme, sáng/tối, mật độ, workspace
└─ dist/                   file sinh ra (không sửa tay)
   ├─ suite.css            base + theme default + component (dùng nhanh)
   ├─ base.css, components.css
   ├─ themes/<id>.css      một file cho mỗi theme (production)
   ├─ themes.all.css       mọi theme, gắn theo [data-brand] (preview, console)
   ├─ tailwind.css         ánh xạ token sang Tailwind v4
   ├─ tokens.json          giá trị đã giải của mọi theme + kết quả kiểm tra tương phản
   └─ themes.index.js      dữ liệu cho trang demo
```

## 3. Lệnh

```powershell
node tools/build.mjs
node tools/build.mjs new-theme --id acme --name "Acme" --primary "#0b6e4f" --accent "#b45309"
node tools/build.mjs new-theme --id acme-gov --primary "#1e3a8a" --style flat --density compact --radius 4 --font "Noto Sans"
python -m http.server 4173 --directory .
```

Lệnh cuối mở demo tại `http://localhost:4173/demo/`.

`build` dừng với mã lỗi 1 khi theme có một trong các lỗi sau:
- Thiếu token, hoặc có token lạ.
- Màu sai định dạng, hoặc có alpha ở token không được phép.
- Style hoặc chế độ mặc định không hợp lệ.
- **Không đạt một cặp tương phản** trong `contract.json` (chữ 4.5:1; viền control và vòng focus 3:1; ở cả 2 chế độ).

Token có alpha được chồng lên "ground" của nó trước khi đo tương phản. Riêng **kính** (`surface-glass`) được đo trên **từng màu lấy từ `backdrop`**, và kết quả là trường hợp xấu nhất.

## 4. Tạo theme cho khách hàng mới

1. Chạy `new-theme` với màu thương hiệu.
   - Mặc định theme mới kế thừa `default` (kính). Muốn kiểu phẳng thì thêm `--style flat` (kế thừa `classic`).
   - Công cụ tự suy ra cho cả 2 chế độ: `primary`, `primary-hi` (đỉnh gradient), `primary-hover`, `primary-fg`, `primary-soft`, `primary-text`, `focus`, `glow`, `chart-1` và `primary-fill`, sao cho đạt mọi cặp tương phản.
2. Màu thương hiệu quá sáng (vàng, xanh lá mạ) sẽ bị làm đậm lên ở chế độ sáng, để nút và vòng focus vẫn nhìn rõ. Muốn màu sáng xuất hiện thì truyền màu đó vào `--accent`.
3. Muốn chỉnh thêm, sửa `themes/<id>.json`:
   - `modes.light` / `modes.dark`: màu, `backdrop`.
   - `theme`: font, bo góc, blur.
   - `components`: ghi đè từng component token, ví dụ `"tab-active-bg": "var(--surface-3)"`.

   Giá trị khai báo tay luôn thắng giá trị suy ra.
4. Chạy `build` và mở demo để xem. Ô màu viền đứt trong demo là token được suy ra.
5. Font phải nằm trong `tokens/base.json → fontWhitelist` (đã kiểm tra đủ dấu tiếng Việt).

Không có CSS tự do theo khách hàng. Theme chỉ được khai báo token có trong `contract.json`.

## 5. Dùng trong ứng dụng Angular

```jsonc
// angular.json → styles (thứ tự quan trọng)
"styles": [
  "node_modules/@suite/design-system/dist/base.css",
  "node_modules/@suite/design-system/dist/components.css",
  "src/styles.css"
]
```

Theme nạp bằng `<link id="suite-theme" href="assets/themes/<id>.css">` (deployment chọn id).

Thuộc tính trên `<html>`:

| Thuộc tính | Giá trị | Ai đặt |
|---|---|---|
| `data-theme` | `light` · `dark`. **Không đặt = `defaultMode` của theme** (`default` là tối). Design system không tự theo hệ điều hành: user chọn "Theo hệ thống" thì `ThemeService` đọc `matchMedia` rồi đặt `data-theme` | `ThemeService` |
| `data-density` | `comfortable` · `compact` (không đặt = mặc định của theme) | `ThemeService` |
| `data-product` | `crm` · `erp` · `hrm` · `dms` · `bi` · `wf`: đổi `--product` và hiện dải màu trên topbar | Layout của workspace |
| `data-brand` | id theme | Chỉ dùng với `themes.all.css` (demo, console xem trước) |

**Tailwind v4** (tùy chọn, chỉ dùng cho bố cục): `@import "tailwindcss"; @import "@suite/design-system/tailwind.css";`. Bảng màu của Tailwind bị xóa, chỉ còn màu của Suite.

Component Angular (`@suite/ui`) render markup dùng class `s-*` và bổ sung hành vi (CDK overlay, bàn phím, ARIA). Không viết style hình thức trong Angular.

### Điều hướng

Sidebar luôn có **đủ các vùng**. Mở một trang không bao giờ làm mất các vùng khác.

```
.s-sidebar
  button.s-switcher        sản phẩm đang mở + popover chọn sản phẩm khác (chỉ có 1 sản phẩm thì dùng .s-brand)
  nav.s-nav                (motion.mjs → pill() vẽ highlight trượt)
    .s-nav-section         Chung: Trang chủ, Chờ duyệt (n), Thông báo
    .s-nav-section         Workspace đang mở: một .s-nav-group cho mỗi module, mục có icon
    .s-nav-section         Cài đặt (theo quyền): Người dùng, Vai trò, Tổ chức, …
  .s-sidebar__foot         tài khoản, hiển thị
```

- Mục menu: `a.s-nav-item` > `svg.s-ico` + `span.s-nav-item__label` + (tùy chọn) `.s-count`. Mục đang mở có `aria-current="page"`.
- Mỗi route khai báo nó thuộc vùng nào. **Không đoán vùng từ đoạn đầu URL.** Tiêu đề topbar lấy từ tên trang, không lấy từ URL.
- Desktop thu gọn thành rail (chỉ icon) bằng `.s-shell--rail`.
- Trang dạng cây (tổ chức, danh mục) dùng `.s-split`:
  - Bên trái: `.s-tree` (`role="tree"`, `aria-level`, `aria-expanded`, `aria-selected`).
  - Bên phải: card chi tiết.
  - Trên điện thoại: `.s-list` đi sâu từng cấp, có breadcrumb.

### Chuyển động

Chuyển từ motion kit của Halvo, nhanh và nhẹ hơn cho màn hình nghiệp vụ. Tất cả tắt khi người dùng bật `prefers-reduced-motion`.

| Hiệu ứng | Cách dùng |
|---|---|
| Card, KPI, tile nổi lên lần lượt | `.s-motion-rise` trên container (CSS, stagger 50ms) |
| Dòng danh sách trượt vào | `.s-motion-slide` |
| Tile nhấc lên khi hover | `.s-lift` |
| Popover, menu bật ra | Tự có |
| Pill trượt (tab, segmented, sidebar, thanh tab ở đáy) | `pill(track)` trong `dist/motion.mjs` (export `@suite/design-system/motion`); Angular bọc thành directive `suitePill` |
| Số đếm lên | `countTo(el, value, { format, flash })`; Angular: `[suiteCount]` |
| Chuyển trang | View Transitions API: `provideRouter(routes, withViewTransitions({ skipInitialTransition: true }))`. Chỉ vùng `.s-content` di chuyển |

Quy tắc:
- Không làm hiệu ứng cho từng dòng bảng mỗi lần lọc hoặc đổi trang dữ liệu.
- Không làm hiệu ứng cho blur, kích thước hay màu. Chỉ làm cho transform, opacity, clip-path.
- Vào thì dùng ease-out (`--ease-expo`). Ra thì dùng ease-in, thời gian khoảng 1/3 lúc vào. Thứ nhỏ (popover, badge) dùng `--ease-spring`.

## 6. Quy tắc thiết kế

- **Kính chỉ dành cho khung ứng dụng và dashboard.**
  - Có blur: sidebar, topbar, thanh tab, dialog, menu, popover, toast, `.s-card--glass` (KPI, page head, tile, card đăng nhập).
  - Không blur, gần đặc: bề mặt chứa dữ liệu `.s-card` (bảng, form, danh sách). Không bọc một bảng dài trong `.s-card--glass`.
  - Khi người dùng bật `prefers-reduced-transparency`, mọi kính thành đặc.
- **Một hành động chính mỗi màn hình** (`.s-btn--primary`, nền gradient và quầng sáng). Teal chỉ để đánh dấu thứ đang bật, đang chọn hoặc là hành động chính, không dùng để trang trí.
- **Màu trạng thái chỉ dùng cho trạng thái**, và luôn đi kèm chữ hoặc icon.
- **Chữ:** Be Vietnam Pro. Thân chữ đậm 500, control và tiêu đề 600. Số dùng `tabular-nums`. Đơn vị đứng sau con số, cỡ nhỏ hơn và màu `muted`: `248 người`, `15.000.000 ₫`.
- **Bo góc lồng nhau:** con luôn nhỏ hơn cha. `radius-xl` cho sidebar và dialog, `lg` cho card, `md` cho nút và input, `sm` cho ô nhỏ.
- **Mật độ có 2 mức.** Trên thiết bị cảm ứng, control tối thiểu 44px, input 16px.
- **Responsive:**
  - Breakpoint 640 / 768 / 1024 / 1280.
  - Dưới 1024px, sidebar thành drawer.
  - Dưới 768px, dialog thành bottom sheet có tay nắm, và cổng tự phục vụ có thanh tab nổi ở đáy.
  - Bảng `.s-table--stack` thành thẻ khi khung hẹp hơn 640px.
- **Trang đăng nhập** dùng `.s-auth`:
  - Một cột, card ở giữa, logo phía trên.
  - Nút submit rộng hết card và **không bị vô hiệu hóa**: kiểm tra lỗi khi submit.
  - Lỗi đăng nhập hiện bằng `.s-alert` phía trên các field.
  - Link "Quên mật khẩu?" nằm cạnh label của mật khẩu.
- **Accessibility:** focus 2px `--focus`. Mọi cặp màu trong `contract.json` được kiểm tra tự động. Tôn trọng `prefers-reduced-motion` và `prefers-reduced-transparency`.
- **Icon:** demo dùng Lucide (ISC), nét mảnh, hợp với kính. Cần chốt với kế hoạch Business Suite (câu hỏi Q5).

## 7. Version

Version nằm trong `package.json`, thay đổi ghi vào `CHANGELOG.md`, tag dạng `suite@X.Y.Z`.

- **Theme khách hàng là dữ liệu:** thêm hoặc sửa theme khách hàng không làm đổi version của core.
- **Minor:** thêm token, thêm style preset, thêm class `s-*`.
- **Major** (sau 1.0): đổi tên hoặc xóa token trong `contract.json`, hoặc đổi tên class `s-*`.
