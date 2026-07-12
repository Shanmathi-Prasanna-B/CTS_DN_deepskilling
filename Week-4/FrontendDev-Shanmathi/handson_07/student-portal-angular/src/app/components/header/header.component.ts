import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <header class="header">
      <h1>{{ siteName }}</h1>
      <nav>
        <a routerLink="/">Courses</a>
        <a routerLink="/profile">Profile</a>
      </nav>
    </header>
  `,
  styles: [`
    .header { display: flex; justify-content: space-between; align-items: center; padding: 20px 40px; background: #1e3a8a; color: #fff; }
    nav { display: flex; gap: 16px; }
    a { color: #fff; text-decoration: none; }
  `],
})
export class HeaderComponent {
  @Input() siteName = 'Student Portal';
}
