//! \file
/*
**  Copyright (C) - Triton
**
**  This program is under the terms of the BSD License.
*/

#include <iosfwd>                         // for ostream
#include <string>                         // for string
#include <triton/astRepresentation.hpp>   // for AstRepresentation, astRepre...
#include <triton/astContext.hpp>          // for AstContext
#include <triton/exceptions.hpp>          // for SymbolicExpression
#include <triton/symbolicExpression.hpp>  // for SymbolicExpression
#include "triton/ast.hpp"                 // for AbstractNode, newInstance
#include "triton/symbolicEnums.hpp"       // for symkind_e, symkind_e::MEM
#include "triton/tritonTypes.hpp"         // for usize


namespace triton {
  namespace engines {
    namespace symbolic {

      SymbolicExpression::SymbolicExpression(triton::ast::AbstractNode* node, triton::usize id, symkind_e kind, const std::string& comment)
        : originRegister() {
        this->comment       = comment;
        this->ast           = node;
        this->id            = id;
        this->isTainted     = false;
        this->kind          = kind;
      }


      triton::ast::AbstractNode* SymbolicExpression::getAst(void) const {
        if (this->ast == nullptr)
          throw triton::exceptions::SymbolicExpression("SymbolicExpression::getAst(): No AST defined.");
        return this->ast;
      }


      triton::ast::AbstractNode* SymbolicExpression::getNewAst(void) const {
        if (this->ast == nullptr)
          throw triton::exceptions::SymbolicExpression("SymbolicExpression::getNewAst(): No AST defined.");
        return triton::ast::newInstance(this->ast);
      }


      const std::string& SymbolicExpression::getComment(void) const {
        return this->comment;
      }


      triton::usize SymbolicExpression::getId(void) const {
        return this->id;
      }


      std::string SymbolicExpression::getFormattedId(void) const {
        if (this->ast == nullptr)
          throw triton::exceptions::SymbolicExpression("SymbolicExpression::getFormattedId(): No AST defined.");
        if (ast->getContext().getRepresentationMode() == triton::ast::representations::SMT_REPRESENTATION)
          return "ref!" + std::to_string(this->id);

        else if (ast->getContext().getRepresentationMode() == triton::ast::representations::PYTHON_REPRESENTATION)
          return "ref_" + std::to_string(this->id);

        else
          throw triton::exceptions::SymbolicExpression("SymbolicExpression::getFormattedId(): Invalid AST representation mode.");
      }


      std::string SymbolicExpression::getFormattedComment(void) const {
        if (this->ast == nullptr)
          throw triton::exceptions::SymbolicExpression("SymbolicExpression::getFormattedComment(): No AST defined.");
        if (this->getComment().empty())
          return "";

        else if (ast->getContext().getRepresentationMode() == triton::ast::representations::SMT_REPRESENTATION)
          return "; " + this->getComment();

        else if (ast->getContext().getRepresentationMode() == triton::ast::representations::PYTHON_REPRESENTATION)
          return "# " + this->getComment();

        else
          throw triton::exceptions::SymbolicExpression("SymbolicExpression::getFormattedComment(): Invalid AST representation mode.");
      }


      symkind_e SymbolicExpression::getKind(void) const {
        return this->kind;
      }


      const triton::arch::MemoryAccess& SymbolicExpression::getOriginMemory(void) const {
        return this->originMemory;
      }


      const triton::arch::Register& SymbolicExpression::getOriginRegister(void) const {
        return this->originRegister;
      }


      void SymbolicExpression::setAst(triton::ast::AbstractNode* node) {
        node->setParent(this->ast->getParents());
        this->ast = node;
        this->ast->init();
      }


      void SymbolicExpression::setComment(const std::string& comment) {
        this->comment = comment;
      }


      void SymbolicExpression::setKind(symkind_e k) {
        this->kind = k;
      }


      void SymbolicExpression::setOriginMemory(const triton::arch::MemoryAccess& mem) {
        this->originMemory = mem;
      }


      void SymbolicExpression::setOriginRegister(const triton::arch::Register& reg) {
        this->originRegister = reg;
      }


      bool SymbolicExpression::isRegister(void) const {
        return (this->kind == triton::engines::symbolic::REG);
      }


      bool SymbolicExpression::isMemory(void) const {
        return (this->kind == triton::engines::symbolic::MEM);
      }


      bool SymbolicExpression::isSymbolized(void) const {
        if (this->ast == nullptr)
          return false;
        return this->ast->isSymbolized();
      }


      std::ostream& operator<<(std::ostream& stream, const SymbolicExpression& symExpr) {
        stream << symExpr.getFormattedId() << " = " << symExpr.getAst();
        if (!symExpr.getComment().empty())
          stream << " " << symExpr.getFormattedComment();
        return stream;
      }


      std::ostream& operator<<(std::ostream& stream, const SymbolicExpression* symExpr) {
        stream << *symExpr;
        return stream;
      }

    }; /* symbolic namespace */
  }; /* engines namespace */
}; /*triton namespace */

