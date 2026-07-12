import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CourseCardComponent } from '../course-card/course-card.component';
import { CourseService } from '../../services/course.service';

@Component({
  selector: 'app-course-list',
  standalone: true,
  imports: [CommonModule, FormsModule, CourseCardComponent],
  template: `
    <section>
      <h2>Courses</h2>
      <input type="text" [(ngModel)]="searchTerm" placeholder="Search courses..." />
      <p *ngIf="loading">Loading...</p>
      <p *ngIf="!loading && filteredCourses.length === 0">No courses found</p>
      <div class="course-grid">
        <app-course-card
          *ngFor="let course of filteredCourses"
          [name]="course.name"
          [code]="course.code"
          [credits]="course.credits"
          [grade]="course.grade">
        </app-course-card>
      </div>
    </section>
  `,
  styles: [`
    .course-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 20px; }
    input { width: 100%; padding: 10px; margin-bottom: 16px; }
  `],
})
export class CourseListComponent implements OnInit {
  courses: any[] = [];
  searchTerm = '';
  loading = true;

  private fallback = [
    { name: 'Data Structures', code: 'CS101', credits: 4, grade: 'A' },
    { name: 'Database Management', code: 'CS201', credits: 3, grade: 'B+' },
    { name: 'Web Development', code: 'CS301', credits: 4, grade: 'A-' },
    { name: 'Operating Systems', code: 'CS401', credits: 3, grade: 'B' },
    { name: 'Computer Networks', code: 'CS501', credits: 3, grade: 'A' },
  ];

  constructor(private courseService: CourseService) {}

  ngOnInit(): void {
    this.courseService.getCourses().subscribe({
      next: (posts) => {
        this.courses = posts.map((post: any, i: number) => ({
          name: this.fallback[i]?.name || post.title,
          code: this.fallback[i]?.code || `CS${post.id}`,
          credits: this.fallback[i]?.credits || 3,
          grade: this.fallback[i]?.grade || 'B',
        }));
        this.loading = false;
      },
      error: () => {
        this.courses = this.fallback;
        this.loading = false;
      },
    });
  }

  get filteredCourses() {
    return this.courses.filter((c) =>
      c.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }
}
