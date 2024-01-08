// From the software distribution accompanying the textbook
// "A Practical Introduction to Data Structures and Algorithm Analysis,
// Third Edition (C++)" by Clifford A. Shaffer.
// Source code Copyright (C) 2007-2011 by Clifford A. Shaffer.
// 1/26/22 pragma once modification by Prof Sipantzi
// 2/18/22 printHelp(), insertHelp(), printInorder(), printReverse()
// -----modification by Aidan Jones for Quadtree functionality (the original code was a binary tree)

#include "QuadNode.h"
#include <iostream>

#pragma once

template <typename E> class ImageQuadtree
{
private:
	QuadNode<E>* root;
    int nodecount;
    int w; //width
    int h; //height

    void clearhelp(QuadNode<E>*);
    QuadNode<E>* inserthelp(QuadNode<E>*, const Point&, const E&);
    QuadNode<E>* removehelp(QuadNode<E>*, const Point&);
    E* findhelp(QuadNode<E>*, const Point&) const;
    void printhelp(QuadNode<E>*, int) const;

public:
    ImageQuadtree() { root = NULL; nodecount = 0; } //Constructor
    
    ~ImageQuadtree() { clearhelp(root); }

    void clear() {
        clearhelp(root);
        root = NULL;
        nodecount = 0;
    }

    void insert(const Point& p, const E& e) {
        root = inserthelp(root, p, e);
        nodecount++;
    }

    E* remove(const Point& p) {
        E* temp = findhelp(root, p);
        if (temp != NULL) {
            root = removehelp(root, p);
            nodecount--;
        }
        return temp;
    }

    E* find(const Point& p) const { return findhelp(root, p); }

    int size() { return nodecount; }

    void print() const {
        if (root == NULL) cout << "The QuadTree is empty.\n";
        else printhelp(root, 0);
    }

    void compress();
    void fromArray();
    void toArray();
};

// Clean up Quadtree by releasing space back free store
template <typename E> void ImageQuadtree<E>::clearhelp(QuadNode<E>* root) {
    if (root == NULL) return;
    clearhelp(root->topLeft());
    clearhelp(root->topRight());
    clearhelp(root->botLeft());
    clearhelp(root->botRight());
    delete root;
}

// Insert a node into the Quadtree, returning the updated tree
template <typename E> QuadNode<E>* ImageQuadtree<E>::inserthelp(QuadNode<E>* root, const Point& p, const E& e) {
    if (root == NULL)  // Empty tree: create node
        return new QuadNode<E>(p, e, NULL, NULL, NULL, NULL);
    if (p.x < root->location().x) //left portion
    {
        if (p.y < root->location().y) //bottom portion
        {
            if (root->botLeft() == NULL)
                root->setBotLeft(new QuadNode<E>(p, e));
            else
                root->setBotLeft(inserthelp(root->botLeft(), p, e));
        }
        else //top portion
        {
            if (root->topLeft() == NULL)
                root->setTopLeft(new QuadNode<E>(p, e));
            else
                root->setTopLeft(inserthelp(root->topLeft(), p, e));
        }
    }
    else //right portion
    {
        if (p.y < root->location().y) //bottom portion
        {
            if (root->botRight() == NULL)
                root->setBotRight(new QuadNode<E>(p, e));
            else
                root->setBotRight(inserthelp(root->botRight(), p, e));
        }
        else //top portion
        {
            if (root->topRight() == NULL)
                root->setTopRight(new QuadNode<E>(p, e));
            else
                root->setTopRight(inserthelp(root->topRight(), p, e));
        }
    }
    return root; // Return tree with node inserted
}

// Remove a node with key value k
// Return: The tree with the node removed
template <typename E> QuadNode<E>* ImageQuadtree<E>::removehelp(QuadNode<E>* root, const Point& p) {
    if (root == NULL) return NULL;    // k is not in tree
    else if (p.x < root->location().x) {
        if (p.y < root->location().y)
            root->setBotLeft(removehelp(root->botLeft(), p));
        else
            root->setTopLeft(removehelp(root->topLeft(), p));
    }
    else if (p.x > root->location().x) {
        if (p.y < root->location().y)
            root->setBotRight(removehelp(root->botRight(), p));
        else
            root->setTopRIght(removehelp(root->topRight(), p));
    }
    else {                            // Found: remove it
        QuadNode<E>* temp = root;
        if (root->left() == NULL) {     // Only a right child
            root = root->right();         //  so point to right
            delete temp;
        }
        else if (root->right() == NULL) { // Only a left child
            root = root->left();          //  so point to left
            delete temp;
        }
        else {                    // Both children are non-empty
            BSTNode<Key, E>* temp = getmin(root->right());
            root->setElement(temp->element());
            root->setKey(temp->key());
            root->setRight(deletemin(root->right()));
            delete temp;
        }
    }
    return root;
}

// Find a node with the given key value
template <typename E> E* ImageQuadtree<E>::findhelp(QuadNode<E>* root, const Point& p) const
{
    if (root == NULL) return NULL; // Empty tree
    // Check left
    if (p.x < root->location().x) {
        if (p.y < root->location().y) // Check bottom
            return findhelp(root->botLeft(), p);
        else //Check top
            return findhelp(root->topLeft(), p);
    }
    // Check right
    else if (k > root->key()) {  
        if (p.y < root->location().y) // Check bottom
            return findhelp(root->botRight(), p);
        else //Check top
            return findhelp(root->topRight(), p);
    }
    else {
        E* temp = new E;
        *temp = root->element();
        return temp;  // Found it
    }
}

// Print out a Quadtree
template <typename E> void ImageQuadtree<E>::printhelp(QuadNode<E>* root, int level) const {
    if (root == NULL) return;           // Empty tree
    printhelp(root->left(), level + 1); // Do left subtree
    for (int i = 0; i < level; i++)     // Indent to level
        cout << "  ";
    cout << root->key() << "\n";        // Print node value
    printhelp(root->right(), level + 1);// Do right subtree
}
