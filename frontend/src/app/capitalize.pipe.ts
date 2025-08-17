import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'capitalize'
})
export class CapitalizePipe implements PipeTransform {
  transform(value: string | undefined, allWords: boolean = false): string {
    if (!value) return '';
    if (allWords) {
      return value.replace(/\b\w/g, char => char.toUpperCase());
    }
    return value.charAt(0).toUpperCase() + value.slice(1);
  }
}
