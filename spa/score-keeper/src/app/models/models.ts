
export interface BaseModel {
    id?: string;
    created_at?: string;
    updated_at?: string;
}

export interface Priviledge extends BaseModel {
    priviledge_name: string;
  }

export interface Role extends BaseModel {
    role_name: string;
    priviledges: Priviledge[];
}

export interface User extends BaseModel {
    username?: string;
    firstname?: string;
    lastname?: string;
    email?: string;
    role?: Role;
    account_locked?: boolean;
    last_login?: string;
}

export interface Grade extends BaseModel {
    grade_name: string;
    grade_value: number;
}

export interface StudentGroup extends BaseModel {
    group_name: string;
    grades: Grade[];
}

export interface Student extends BaseModel {
    firstname: string;
    lastname: string;
    grade: Grade;
    student_group: StudentGroup;
}

export interface Interval {
    repeat: 'daily' | 'weekly' | 'monthly' | 'none';
    month_day?: number;
    week_day?: number;
    hour?: number;
    minute?: number;
}

export interface PointCategory extends BaseModel {
    category_name: string;
    description: string;
    deleted: boolean;
}

export interface Point extends BaseModel {
    points: number;
    student_group: StudentGroup;
    points_interval: String;
    point_category: PointCategory;
    deleted: boolean;
}

export interface Event extends BaseModel {
    event_name: string;
    interval: Interval;
    deleted: boolean;
    completed: boolean;
    student_groups: StudentGroup[];
    point_categories: PointCategory[];
}

export interface EventInstance extends BaseModel {
    event: Event;
    event_date: string;
    completed: boolean;
    deleted: boolean;
}

export interface PointEarned extends BaseModel {
    student: Student;
    event_instance: EventInstance;
    points: Point;
    deleted: boolean;
}

export interface PointSpent extends BaseModel {
    student: Student;
    event_instance: EventInstance;
    points: number;
    deleted: boolean;
}

export interface RunningTotal extends BaseModel {
    student: Student;
    total_points: number;
}