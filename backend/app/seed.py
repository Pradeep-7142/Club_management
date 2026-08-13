import os
import bcrypt
from datetime import datetime, timezone
from app.extensions import db
from app.models import (
    Club,
    ClubMember,
    Event,
    GalleryImage,
    Notification,
    User,
)


def _hash(pw: str) -> str:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def seed_database(force: bool = False):
    """Seed comprehensive realistic data for all platform features."""
    if not force and User.query.first():
        return

    # Clear existing records if force seeding
    if force:
        db.session.query(GalleryImage).delete()
        db.session.query(Event).delete()
        db.session.query(ClubMember).delete()
        db.session.query(Notification).delete()
        db.session.query(Club).delete()
        db.session.query(User).delete()
        db.session.commit()

    demo_pw = os.environ.get("DEMO_PASSWORD", "password")
    h = _hash(demo_pw)

    # 1. CORE USERS
    users = [
        # Admin
        ("admin-1", "admin@university.edu", "Dr. Eleanor Vance (Dean & Admin)", "admin", None),
        # Club Heads
        ("head-1", "head@university.edu", "Alex Rivera (Tech Head)", "club_head", "club-tech"),
        ("head-arts", "arts.head@university.edu", "Sophia Chen (Arts Head)", "club_head", "club-arts"),
        ("head-robotics", "robotics.head@university.edu", "Priya Patel (Robotics Head)", "club_head", "club-robotics"),
        ("head-sports", "sports.head@university.edu", "Marcus Johnson (Sports Head)", "club_head", "club-sports"),
        ("head-music", "music.head@university.edu", "Liam O'Connor (Music Head)", "club_head", "club-music"),
        # Students
        ("student-1", "student@university.edu", "Jordan Lee", "student", "club-tech"),
        ("student-2", "emma.watson@university.edu", "Emma Watson", "student", "club-arts"),
        ("student-3", "david.kim@university.edu", "David Kim", "student", "club-sports"),
        ("student-4", "maya.lin@university.edu", "Maya Lin", "student", "club-robotics"),
        ("student-5", "sam.wilson@university.edu", "Sam Wilson", "student", "club-music"),
    ]

    for uid, email, name, role, cid in users:
        db.session.add(
            User(
                id=uid,
                email=email,
                name=name,
                role=role,
                password_hash=h,
                club_id=cid,
            )
        )
    db.session.flush()

    # 2. CLUBS
    clubs = [
        Club(
            id="club-tech",
            name="Tech Innovators Club",
            description="Empowering students through cutting-edge hackathons, software architecture workshops, AI labs, and open-source collaboration.",
            category="Technology",
            member_count=42,
            points=380,
            head_id="head-1",
            logo="https://images.unsplash.com/photo-1518770660439-4636190af475?w=500&auto=format&fit=crop&q=80",
            created_at="2026-01-10",
        ),
        Club(
            id="club-arts",
            name="Creative Arts & Media",
            description="A vibrant collective for graphic designers, digital painters, photographers, 3D sculptors, and creative visual storytellers.",
            category="Arts",
            member_count=35,
            points=290,
            head_id="head-arts",
            logo="https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=500&auto=format&fit=crop&q=80",
            created_at="2026-01-15",
        ),
        Club(
            id="club-robotics",
            name="Robotics & AI Society",
            description="Designing autonomous rovers, competitive combat bots, edge AI systems, and aerial drone avionics.",
            category="Engineering",
            member_count=48,
            points=420,
            head_id="head-robotics",
            logo="https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=500&auto=format&fit=crop&q=80",
            created_at="2026-01-12",
        ),
        Club(
            id="club-sports",
            name="Campus Athletics & Esports",
            description="Fostering teamwork, physical fitness, intra-university leagues, and competitive collegiate esports tournaments.",
            category="Sports",
            member_count=56,
            points=310,
            head_id="head-sports",
            logo="https://images.unsplash.com/photo-1511512578047-dfb367046420?w=500&auto=format&fit=crop&q=80",
            created_at="2026-01-20",
        ),
        Club(
            id="club-music",
            name="Harmonix Music Society",
            description="Uniting campus vocalists, instrumentalists, audio engineers, and electronic producers for live stage performances and studio jamming.",
            category="Cultural",
            member_count=29,
            points=240,
            head_id="head-music",
            logo="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500&auto=format&fit=crop&q=80",
            created_at="2026-02-01",
        ),
        Club(
            id="club-eco",
            name="Green Campus & Sustainability",
            description="Leading zero-waste campus initiatives, solar energy workshops, botanical gardens, and community environmental impact projects.",
            category="Social",
            member_count=24,
            points=190,
            head_id="head-1",
            logo="https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=500&auto=format&fit=crop&q=80",
            created_at="2026-02-10",
        ),
    ]
    db.session.add_all(clubs)
    db.session.flush()

    # 3. MEMBERSHIPS
    memberships = [
        # Tech Club
        ClubMember(user_id="head-1", club_id="club-tech"),
        ClubMember(user_id="student-1", club_id="club-tech"),
        ClubMember(user_id="student-3", club_id="club-tech"),
        ClubMember(user_id="student-4", club_id="club-tech"),
        # Arts Club
        ClubMember(user_id="head-arts", club_id="club-arts"),
        ClubMember(user_id="student-1", club_id="club-arts"),
        ClubMember(user_id="student-2", club_id="club-arts"),
        # Robotics Club
        ClubMember(user_id="head-robotics", club_id="club-robotics"),
        ClubMember(user_id="student-1", club_id="club-robotics"),
        ClubMember(user_id="student-4", club_id="club-robotics"),
        # Sports Club
        ClubMember(user_id="head-sports", club_id="club-sports"),
        ClubMember(user_id="student-3", club_id="club-sports"),
        ClubMember(user_id="student-5", club_id="club-sports"),
        # Music Club
        ClubMember(user_id="head-music", club_id="club-music"),
        ClubMember(user_id="student-2", club_id="club-music"),
        ClubMember(user_id="student-5", club_id="club-music"),
        # Eco Club
        ClubMember(user_id="student-1", club_id="club-eco"),
    ]
    db.session.add_all(memberships)

    # 4. EVENTS (Approved, Pending, Past, Future)
    events = [
        # Approved Events
        Event(
            id="event-hackathon",
            title="Annual HackMatrix 2026 Hackathon",
            description="36-hour hackathon focused on Generative AI, Web3, and Sustainable Smart Cities. Mentors from top tech companies and $10k in prize pool.",
            date="2026-05-20",
            time="09:00 AM",
            location="Innovation Hub & Grand Auditorium",
            club_id="club-tech",
            status="approved",
            created_by="head-1",
            attendance_count=145,
        ),
        Event(
            id="event-art-expo",
            title="Spring Visual Arts & Digital Media Gallery",
            description="Exhibition displaying student oil paintings, digital art concepts, UI/UX showcases, and interactive 3D virtual installations.",
            date="2026-05-28",
            time="11:00 AM",
            location="Central Fine Arts Gallery, Wing C",
            club_id="club-arts",
            status="approved",
            created_by="head-arts",
            attendance_count=92,
        ),
        Event(
            id="event-robotics-showcase",
            title="Autonomous Drone & BattleBot Arena 2026",
            description="High-octane obstacle course racing for autonomous quadcopters and competitive 3lb combat bot arena tournament.",
            date="2026-06-05",
            time="02:00 PM",
            location="Engineering Quadrangle Outdoor Field",
            club_id="club-robotics",
            status="approved",
            created_by="head-robotics",
            attendance_count=118,
        ),
        Event(
            id="event-esports",
            title="Inter-College Esports Invitational (Valorant & Rocket League)",
            description="Live-streamed esports championship on campus big screens with shoutcasting, team rivalries, and custom tournament trophies.",
            date="2026-06-12",
            time="05:00 PM",
            location="Student Union Esports Arena",
            club_id="club-sports",
            status="approved",
            created_by="head-sports",
            attendance_count=180,
        ),
        Event(
            id="event-sunset-jam",
            title="Acoustic Sunset Concert & Open Mic",
            description="An evening of acoustic indie covers, jazz fusion, and original student songs under the campus sunset.",
            date="2026-06-18",
            time="06:30 PM",
            location="Campus Amphitheater Lawn",
            club_id="club-music",
            status="approved",
            created_by="head-music",
            attendance_count=78,
        ),
        Event(
            id="event-past-ai",
            title="Deep Learning & LLM Fine-Tuning Bootcamp",
            description="Hands-on workshop training Hugging Face transformer models using university GPU clusters.",
            date="2026-03-12",
            time="03:00 PM",
            location="Computer Science Lab 304",
            club_id="club-tech",
            status="approved",
            created_by="head-1",
            attendance_count=85,
        ),
        Event(
            id="event-past-photo",
            title="Golden Hour Campus Photography Walk",
            description="Practical tutorial on camera aperture, framing architectural lighting, and Adobe Lightroom mobile color grading.",
            date="2026-03-25",
            time="04:30 PM",
            location="Bell Tower Plaza",
            club_id="club-arts",
            status="approved",
            created_by="head-arts",
            attendance_count=48,
        ),
        # Pending Events (For testing Admin approval and Club Head tracking)
        Event(
            id="event-pending-cloud",
            title="Cloud Native Architecture & Kubernetes Bootcamp",
            description="Deploying microservices and configuring autoscaling CI/CD pipelines with Kubernetes and Terraform.",
            date="2026-07-02",
            time="10:00 AM",
            location="Innovation Lab Room 202",
            club_id="club-tech",
            status="pending",
            created_by="head-1",
            attendance_count=50,
        ),
        Event(
            id="event-pending-vr",
            title="Spatial Audio & Virtual Reality Cinema Experience",
            description="Interactive workshop exploring Unreal Engine 5 spatial environments and Apple Vision / Meta Quest interactive cinema.",
            date="2026-07-10",
            time="01:30 PM",
            location="Media Arts Studio 105",
            club_id="club-arts",
            status="pending",
            created_by="head-arts",
            attendance_count=35,
        ),
        Event(
            id="event-pending-3v3",
            title="Summer 3v3 Street Basketball Tournament",
            description="Fast-paced double elimination 3v3 half-court basketball tournament with music, refreshments, and MVP awards.",
            date="2026-07-15",
            time="04:00 PM",
            location="Recreation Center Outdoor Courts",
            club_id="club-sports",
            status="pending",
            created_by="head-sports",
            attendance_count=60,
        ),
        # Rejected Event
        Event(
            id="event-rejected-midnight",
            title="Midnight Rooftop Fireworks & Drone Light Show",
            description="Synchronized drone swarm light show over university bell tower at midnight.",
            date="2026-07-28",
            time="11:45 PM",
            location="Main Science Building Roof",
            club_id="club-robotics",
            status="rejected",
            created_by="head-robotics",
            attendance_count=0,
        ),
    ]
    db.session.add_all(events)
    db.session.flush()

    # 5. GALLERY IMAGES
    gallery = [
        GalleryImage(
            id="img-1",
            event_id="event-hackathon",
            url="https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&auto=format&fit=crop&q=80",
            uploaded_at="2026-04-10T10:00:00",
        ),
        GalleryImage(
            id="img-2",
            event_id="event-hackathon",
            url="https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800&auto=format&fit=crop&q=80",
            uploaded_at="2026-04-10T11:30:00",
        ),
        GalleryImage(
            id="img-3",
            event_id="event-art-expo",
            url="https://images.unsplash.com/photo-1561214115-f2f134cc4912?w=800&auto=format&fit=crop&q=80",
            uploaded_at="2026-04-12T14:00:00",
        ),
        GalleryImage(
            id="img-4",
            event_id="event-art-expo",
            url="https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=800&auto=format&fit=crop&q=80",
            uploaded_at="2026-04-12T16:00:00",
        ),
        GalleryImage(
            id="img-5",
            event_id="event-robotics-showcase",
            url="https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&auto=format&fit=crop&q=80",
            uploaded_at="2026-04-14T09:00:00",
        ),
        GalleryImage(
            id="img-6",
            event_id="event-esports",
            url="https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&auto=format&fit=crop&q=80",
            uploaded_at="2026-04-15T18:00:00",
        ),
        GalleryImage(
            id="img-7",
            event_id="event-sunset-jam",
            url="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800&auto=format&fit=crop&q=80",
            uploaded_at="2026-04-16T20:00:00",
        ),
        GalleryImage(
            id="img-8",
            event_id="event-past-ai",
            url="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80",
            uploaded_at="2026-03-13T12:00:00",
        ),
        GalleryImage(
            id="img-9",
            event_id="event-past-photo",
            url="https://images.unsplash.com/photo-1452587925148-ce544e77e70d?w=800&auto=format&fit=crop&q=80",
            uploaded_at="2026-03-26T17:00:00",
        ),
    ]
    db.session.add_all(gallery)

    # 6. NOTIFICATIONS
    notifications = [
        Notification(
            id="notif-1",
            type="announcement",
            title="🎉 Welcome to Spring 2026 Campus Club Fest!",
            message="Discover student clubs, register for upcoming hackathons, art galleries, and sports leagues all across campus.",
            created_at="2026-04-01T09:00:00",
        ),
        Notification(
            id="notif-2",
            type="event_approval",
            title="Event Pending Approval: Cloud Native Bootcamp",
            message="Tech Innovators Club submitted 'Cloud Native Architecture & Kubernetes Bootcamp' for Dean/Admin review.",
            club_id="club-tech",
            created_at="2026-04-15T11:00:00",
        ),
        Notification(
            id="notif-3",
            type="event_approval",
            title="Event Pending Approval: VR Storytelling",
            message="Creative Arts & Media submitted 'Spatial Audio & Virtual Reality Cinema Experience' for approval.",
            club_id="club-arts",
            created_at="2026-04-16T14:30:00",
        ),
        Notification(
            id="notif-4",
            type="announcement",
            title="🏆 Robotics Club reaches 400+ Leadership Points!",
            message="Congratulations to the Robotics & AI Society for their outstanding community achievements this semester.",
            created_at="2026-04-18T16:00:00",
        ),
    ]
    db.session.add_all(notifications)

    db.session.commit()
    print("Successfully seeded database with comprehensive dummy data.")


def seed_if_empty():
    seed_database(force=False)

