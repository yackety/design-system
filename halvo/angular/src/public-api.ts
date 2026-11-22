/*
 * @halvo/angular — Angular bindings for the Halvo design system.
 * Needs @halvo/design-system: dist/halvo.css in "styles" and dist/halvo.js in "scripts" (angular.json).
 */
import { HalvoDialDirective } from './lib/dial.directive';
import { HalvoCountDirective, HalvoLiftDirective, HalvoMagneticDirective, HalvoMotionDirective } from './lib/motion.directive';
import { HalvoPillDirective } from './lib/pill.directive';
import { HalvoSelectDirective } from './lib/select.directive';

export * from './lib/halvo.service';
export * from './lib/select.directive';
export * from './lib/pill.directive';
export * from './lib/dial.directive';
export * from './lib/motion.directive';
export type { MotionProps, UiProps, SelectHandle, DialHandle, DialOptions } from './lib/halvo-api';

/** Every Halvo directive, for a standalone component's `imports`. */
export const HALVO_DIRECTIVES = [
  HalvoSelectDirective,
  HalvoPillDirective,
  HalvoDialDirective,
  HalvoMotionDirective,
  HalvoCountDirective,
  HalvoMagneticDirective,
  HalvoLiftDirective,
] as const;
