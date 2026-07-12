import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-course-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <article class="course-card">
      <h3>{{ name }}</h3>
      <p>{{ code }}</p>
      <p>{{ credits }} credits</p>
      <p>Grade: {{ grade }}</p>
    </article>
  `,
  styles: [`
    .course-card { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
  `],
})
export class CourseCardComponent {
  @Input() name = '';
  @Input() code = '';
  @Input() credits = 0;
  @Input() grade = '';
}
