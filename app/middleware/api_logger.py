from fastapi import Request, Response
from sqlalchemy.orm import Session
from app.models.api_log import APILog
from app.database import get_db
import time
import json
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from starlette.datastructures import Headers

exclude_paths = ["/", "/docs", "/openapi.json"]
class APILoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
       
        # Skip logging for root endpoint
        if request.url.path in exclude_paths:
            return await call_next(request)
        # Start timing the request
        start_time = time.time()
        
        # Get database session
        db: Session = next(get_db())
        
        # Store original request body
        body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                # Create a new request with the same body
                async def receive():
                    return {"type": "http.request", "body": body}
                request._receive = receive
            except Exception as e:
                print(f"Error reading request body: {str(e)}")

        # Create log entry
        log_entry = APILog(
            endpoint=request.url.path,
            method=request.method,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
        )
        
        # Log request headers
        try:
            headers_dict = dict(request.headers.items())
            # Remove sensitive headers
            headers_dict.pop("authorization", None)
            headers_dict.pop("cookie", None)
            log_entry.request_headers = headers_dict
        except Exception:
            log_entry.request_headers = None
        
        # Log request body for POST/PUT/PATCH methods
        if body:
            try:
                log_entry.request_body = json.loads(body)
            except Exception:
                log_entry.request_body = str(body)
        
        # Process the request and catch the response
        try:
            response = await call_next(request)
            log_entry.response_status = response.status_code
            
            # Log response body
            try:
                response_body = []
                async for chunk in response.body_iterator:
                    response_body.append(chunk)
                
                # Combine chunks
                full_body = b''.join(response_body)
              
                # Try to parse response body as JSON
                try:
                    log_entry.response_body = json.loads(full_body)
                except:
                    log_entry.response_body = str(full_body)
                
                # Create new response with the same body
                return Response(
                    content=full_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type
                )
            except Exception as e:
                print(f"Error processing response: {str(e)}")
                log_entry.response_body = None
                return response
                
        except Exception as e:
            log_entry.response_status = 500
            log_entry.response_body = {"error": str(e)}
            response = JSONResponse(
                status_code=500,
                content={"error": "Internal server error"}
            )
        
        finally:
            # Calculate execution time
            log_entry.execution_time = time.time() - start_time
            
            # Save log entry
            try:
                db.add(log_entry)
                db.commit()
            except Exception as e:
                print(f"Failed to save API log: {str(e)}")
                db.rollback()
            finally:
                db.close()
        
        return response