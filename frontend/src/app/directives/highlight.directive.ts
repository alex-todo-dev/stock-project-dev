import { Directive, ElementRef, HostListener, Renderer2 } from '@angular/core';

@Directive({
  selector: '[appHighlight]'
})
export class HighlightDirective {

  constructor(private el: ElementRef, private renderer: Renderer2) {}

  @HostListener('mouseenter') onMouseEnter() {
    this.renderer.setStyle(this.el.nativeElement, 'box-shadow', '0 0 10px rgba(0,0,0,0.5)');
    this.renderer.setStyle(this.el.nativeElement, 'transform', 'scale(1.03)');
    this.renderer.setStyle(this.el.nativeElement, 'border-radius', '12px');
    this.renderer.setStyle(this.el.nativeElement, 'transition', '0.2s ease-in-out');
    this.renderer.setStyle(this.el.nativeElement, 'cursor', 'pointer');
  }

  @HostListener('mouseleave') onMouseLeave() {
    this.renderer.removeStyle(this.el.nativeElement, 'box-shadow');
    this.renderer.removeStyle(this.el.nativeElement, 'transform');
  }

}
