# Suite design system

Design system cho **Business Suite** (CRM, ERP, HRM, DMS, BI, Workflow): giao diện nghiệp vụ nhiều dữ liệu, dùng cả ngày, chạy trên desktop lẫn điện thoại. Mỗi khách hàng có thể có **theme riêng** mà không cần build lại ứng dụng.

> Bản 0.1.0 là bản mẫu để chuẩn hóa cách làm: hợp đồng token, cơ chế theme theo khách hàng, công cụ build có kiểm tra tương phản, CSS component và trang demo. Chưa có công cụ release như `halvo/tools/release.py`.

## 1. Ba lớp: core, theme, brand

| Lớp | Ai tạo | Đổi được gì | Ở đâu | Cần build lại app? |
|---|---|---|---|---|
| **Core** | Team design system | Hợp đồng token, thang chữ, khoảng cách, mật độ, chuyển động, CSS component | `tokens/`, `components/` | Có (ra version mới) |
| **Theme** | Vendor (bạn), cho từng khách hàng | Màu thương hiệu, màu nền trung tính, font (trong danh sách cho phép), bo góc, mật độ mặc định | `themes/<id>.json` → `dist/themes/<id>.css` | **Không** |
| **Brand** | Admin của khách hàng, trên màn hình branding | `brand.primary`, `brand.accent`, bo góc, font | Dữ liệu tenant (`platform.branding`) | **Không** |

Cả 3 lớp đi qua **cùng một hợp đồng token** (`tokens/contract.json`), nên mọi component hiển thị đúng với mọi theme. Đây là điểm khác với cách "mỗi khách hàng một design system riêng": nếu mỗi khách hàng có một gói component riêng, mỗi khách hàng sẽ cần một bản build riêng, trái với nguyên tắc "một codebase, một release cho mọi khách hàng" trong `docs/architecture.html` §16–§17.

Khi chạy thật, mỗi deployment chỉ cần một file CSS theme:

```
GET /branding.css  =  dist/themes/<theme của khách hàng>.css  +  phần ghi đè brand của admin (nếu có)
```

## 2. Cấu trúc

```
suite/
├─ package.json            @suite/design-system, version
├─ tokens/
│  ├─ contract.json        token bắt buộc + công dụng + các cặp tương phản phải đạt
│  └─ base.json            token cố định: thang chữ, khoảng cách, chuyển động, z-index, mật độ, font cho phép
├─ themes/
│  ├─ default.json         theme gốc, khai báo đủ mọi token
│  ├─ evergreen.json       mẫu: chỉ khai báo màu thương hiệu + bo góc + font, phần còn lại được suy ra
│  └─ civic.json           mẫu: khối hành chính, góc vuông, mật độ dày
├─ components/*.css        CSS component, tiền tố s- (s-btn, s-input, s-table…)
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
node tools/build.mjs new-theme --id acme --name "Acme" --primary "#0b6e4f" --accent "#b45309" --radius 8 --font "Inter" --density compact
python -m http.server 4173 --directory .
```

Lệnh thứ ba mở demo tại `http://localhost:4173/demo/`.

`build` dừng với mã lỗi 1 khi một theme thiếu token, có token lạ, sai định dạng màu, hoặc **không đạt một cặp tương phản** trong `contract.json` (chữ 4.5:1, viền control và vòng focus 3:1, ở cả 2 chế độ).

## 4. Tạo theme cho khách hàng mới

1. Chạy `new-theme` với màu thương hiệu của khách hàng. Công cụ tự suy ra `primary`, `primary-hover`, `primary-fg`, `primary-soft`, `primary-text`, `focus` và `chart-1` cho cả chế độ sáng lẫn tối, sao cho đạt mọi cặp tương phản.
2. Màu thương hiệu quá sáng (vàng, xanh lá mạ, xanh da trời nhạt) sẽ bị làm đậm lên ở chế độ sáng, để nút và vòng focus vẫn nhìn rõ trên nền trắng. Nếu khách hàng muốn màu sáng xuất hiện, truyền màu đó vào `--accent`.
3. Muốn chỉnh thêm (nền ấm hơn, viền đậm hơn), sửa `themes/<id>.json` → `modes.light` / `modes.dark`. Giá trị khai báo tay luôn thắng giá trị suy ra.
4. Chạy `build` và mở demo để xem. Ô màu viền đứt trong demo là token được suy ra.
5. Font phải nằm trong `tokens/base.json → fontWhitelist` (đã kiểm tra đủ dấu tiếng Việt). Font khác chỉ sinh cảnh báo, nhưng phải tự kiểm tra dấu trước khi giao cho khách hàng.

Một theme chỉ được khai báo các token có trong `contract.json`. Không có CSS tự do theo khách hàng.

## 5. Dùng trong ứng dụng Angular

```jsonc
// angular.json → styles (thứ tự quan trọng)
"styles": [
  "node_modules/@suite/design-system/dist/base.css",
  "node_modules/@suite/design-system/dist/themes/default.css",
  "node_modules/@suite/design-system/dist/components.css",
  "src/styles.css"
]
```

Khi chạy thật, `themes/default.css` được thay bằng `<link rel="stylesheet" href="/branding.css?v=…">` do server trả về theo khách hàng.

Thuộc tính trên `<html>`:

| Thuộc tính | Giá trị | Ai đặt |
|---|---|---|
| `data-theme` | `light` · `dark` (không đặt = theo hệ điều hành) | `ThemeService`, theo lựa chọn của user |
| `data-density` | `comfortable` · `compact` (không đặt = mặc định của theme) | `ThemeService`, theo lựa chọn của user |
| `data-product` | `crm` · `erp` · `hrm` · `dms` · `bi` · `wf` | Layout của workspace, đổi `--product` |
| `data-brand` | id theme | Chỉ dùng với `themes.all.css` (demo, console xem trước) |

**Tailwind v4** (tùy chọn, dùng cho layout): `@import "tailwindcss"; @import "@suite/design-system/tailwind.css";`. File này xóa bảng màu của Tailwind, chỉ để lại màu của Suite (`bg-surface`, `text-muted`, `border-border`, `bg-primary`…). `rounded-sm|md|lg` và `font-sans` tự lấy giá trị của theme. Không cần prefix, vì class component dùng tiền tố `s-` nên không trùng tên với utility của Tailwind.

Component Angular (`@suite/ui` trong Business Suite) render markup dùng các class `s-*` này và bổ sung hành vi (CDK overlay, bàn phím, ARIA). CSS nằm ở design system, nên theme áp lên mọi component mà không phải sửa code Angular.

## 6. Quy tắc thiết kế

- **Rõ ràng hơn hiệu ứng.** Nền phẳng, viền mảnh, bóng nhẹ. Không dùng glass hay blur cho bảng và form dày dữ liệu.
- **Mật độ có 2 mức.** `comfortable` (control 40px, hàng bảng 48px) và `compact` (32px / 36px). Trên thiết bị cảm ứng, control luôn tối thiểu 44px, input 16px để iOS không tự zoom.
- **Màu có nghĩa.** `primary` cho một hành động chính mỗi màn hình. Màu trạng thái chỉ dùng cho trạng thái, và luôn đi kèm chữ hoặc icon, không dùng màu đơn độc.
- **Số liệu** dùng `tabular-nums` (`.s-num`, `.is-num`), canh phải trong bảng. Tiền theo định dạng `15.000.000 ₫`.
- **Responsive:** breakpoint 640 / 768 / 1024 / 1280. Dưới 1024px sidebar thành drawer. Dưới 768px dialog thành bottom sheet, cổng tự phục vụ có thanh tab ở đáy. Bảng `.s-table--stack` thành thẻ khi khung hẹp hơn 640px (container query, không cần JS).
- **Accessibility:** focus 2px màu `--focus`. Mọi cặp màu trong `contract.json` được kiểm tra tự động. Tôn trọng `prefers-reduced-motion`.
- **Icon:** demo dùng Lucide (ISC), nét mảnh hợp với giao diện phẳng. Kế hoạch Business Suite hiện ghi Font Awesome: cần chốt một bộ.

## 7. Version

Theo quy ước của repo: version trong `package.json`, thay đổi ghi vào `CHANGELOG.md`, tag `suite@X.Y.Z`. **Thêm hoặc sửa một theme khách hàng không làm đổi version của core**, vì theme là dữ liệu. Đổi tên hoặc xóa token trong `contract.json`, hoặc đổi tên class `s-*`, là thay đổi **major**.
