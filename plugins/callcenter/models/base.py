from sqlalchemy.ext.declarative import declarative_base, DeferredReflection


# Initialize database metadata without proper engine (engine will be set latter)
Base = declarative_base(cls=DeferredReflection)
