import os
from typing import List
from urllib.parse import urlparse, unquote

from gi.repository import GObject, Nautilus
from PIL import Image
from rembg import new_session, remove

class ImageActionsMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    
    SUPPORTED_MIME_TYPES = ('image/png', 'image/jpeg', 'image/webp')
    
    def remove_background(
        self,
        menu_item: Nautilus.MenuItem,
        files: list[Nautilus.FileInfo],
    ) -> None:
        # Using lightweight u2net model
        model_name = "u2netp"
        session = new_session(model_name)
        for file in files:
            # Extract file path from URI and root (without file extension) from the path
            file_path = self._get_file_path(file)
            root, _ = os.path.splitext(file_path)
            
            destination_file_path = f"{root}_rembg.png"
            
            # Remove background and save in png format
            with Image.open(file_path) as image:
                image = remove(image, session=session)
                image.save(destination_file_path)
    
    def convert_format(
        self,
        menu_item: Nautilus.MenuItem,
        files: list[Nautilus.FileInfo],
        to_format: str,
    ) -> None:
        for file in files:
            # Skip files for which format conversion isn't needed
            from_format = file.get_mime_type().split('/')[1]
            if from_format == to_format:
                continue
            
            # Extract file path from URI and root (without file extension) from the path
            file_path = self._get_file_path(file)
            root, _ = os.path.splitext(file_path)
            
            destination_file_path = f"{root}.{to_format}"
                
            # Convert to specified format
            with Image.open(file_path) as image:
                image.save(destination_file_path)
    
    def get_file_items(
        self,
        files: List[Nautilus.FileInfo],
    ) -> List[Nautilus.MenuItem]:
        # Make sure that every file is of a supported format
        for file in files:
            if file.get_mime_type() not in self.SUPPORTED_MIME_TYPES:
                return []
        
        # Initialize and activate menu item for background removal
        bg_removal_menu_item = Nautilus.MenuItem(
            name="ImageActions::remove_background",
            label="Remove Background",
        )
        bg_removal_menu_item.connect("activate", self.remove_background, files)
        
        # Initialize menu item for format conversion and activate all the submenu items
        convert_menu_item = Nautilus.MenuItem(
            name="ImageActions::convert_to",
            label="Convert to",
        )
        convert_menu = Nautilus.Menu()
        convert_menu_item.set_submenu(convert_menu)
        
        self._append_format_items(convert_menu_item)
        
        for menu_item in convert_menu.get_items():
            menu_item.connect(
                "activate", 
                self.convert_format, 
                files, # files
                menu_item.props.label.lower(), # to_format
            )
        
        return [
            bg_removal_menu_item,
            convert_menu_item,
        ]
        
    def _append_format_items(
        self,
        menu_item: Nautilus.MenuItem,
    ) -> None:
        """Create menu item based on format for every supported format
        and append it to the submenu attached to the given menu item.

        Args:
            menu_item (Nautilus.MenuItem): Menu item with attached submenu.

        Raises:
            TypeError: The menu item that you pass to this method must have a defined submenu (Nautilus.Menu).
        """
        menu = menu_item.props.menu
        
        if not menu:
            raise TypeError("NoneType encountered. The menu item that you pass to this method must have a defined submenu (Nautilus.Menu).")
        
        for mime_type in self.SUPPORTED_MIME_TYPES:
            file_format = mime_type.split('/')[1]
            submenu_item = Nautilus.MenuItem(
                name=f"{menu_item.props.name}_{file_format}",
                label=file_format.upper(),
            )
            menu.append_item(submenu_item)
    
    def _get_file_path(
        self,
        file: Nautilus.FileInfo,
    ) -> str:
        """Parse file uri into string.

        Args:
            file (Nautilus.FileInfo): A nautilus file object.

        Returns:
            str: Parsed string.
        """
        return unquote(urlparse(file.get_uri()).path)
    